from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from inspeakers.models import *

# Create your views here.
def home(request):
    context_dict = get_speakers(request, 'name', None)
    context_dict['page']['url'] = 'home'
    return render(request, 'inspeakers/home.html', context_dict)

def rate(request):
    context_dict = get_speakers(request, 'rate', None)
    context_dict['page']['url'] = 'home/rate'
    return render(request, 'inspeakers/home.html', context_dict)

def tag(request, tag_name_slug):
    context_dict = get_speakers(request, 'name', tag_name_slug)
    context_dict['page']['url'] = 'home/tag/'+tag_name_slug
    return render(request, 'inspeakers/home.html', context_dict)


def get_speakers(request, order, tag):
    page = request.GET.get('page')
    max_result = request.GET.get('max_result')
    if max_result is None:
        max_result = 3
    else:
        max_result = int(max_result)
    if page is None:
        page = 1
    else:
        page = int(page)
    if order is None:
        order='name'
    if tag is None:
        speakers = SpeakerProfile.objects.order_by(order)
    else:
        t = Tag.objects.get(slug=tag)
        speakers = SpeakerProfile.objects.filter(tags=t).order_by(order)
    try:
        context_dict = {'speakers': speakers[(page-1)*max_result: (page)*max_result]}
    except:
        context_dict = {}
    if page <= 1:
        context_dict['page'] = {'previous':1}
    else:
        context_dict['page'] = {'previous':page-1}
    num = int(len(speakers)/max_result)
    if len(speakers)%max_result > 0:
        num += 1
    context_dict['page']['next'] = page + 1
    pages = []
    if num >= page + 2:
        pages.append({'num': page})
        pages.append({'num': page + 1})
        pages.append({'num': page + 2})
    elif num == page + 1:
        if page - 1 > 0:
            pages.append({'num': page - 1})
        pages.append({'num': page})
        pages.append({'num': page + 1})
    elif num <= page:
        if num - 2 > 0:
            pages.append({'num': num - 2})
        if num - 1 > 0:
            pages.append({'num': num - 1})
        pages.append({'num': num})
        context_dict['page']['next'] = num
    context_dict['pages'] = pages
    return context_dict

def speakerprofile(request, speaker_profile_slug):
    s = SpeakerProfile.objects.get(slug = speaker_profile_slug)
    context_dict={}
    context_dict['speaker'] = s
    return render(request,'inspeakers/speakerprofile.html',context_dict)

def post_detail(request, slug):
    template_name = 'post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True) # retrieves all approved comments from the database
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, {'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})

def sign_up(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'inspeakers/signup.html')
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('psw')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('inspeakers:home'))
            else:
                return HttpResponse("Your Inspeakers account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'inspeakers/login.html')

@login_required
def my_account(request):
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == 'POST':
        newname = request.POST.get('username')
        newpsw = request.POST.get('password')
        print(request.FILES)
        if newname is not "":
            user.username = newname
        if newpsw is not "":
            user.set_password(newpsw)
        if 'profile_photo' in request.FILES:
            profile.picture = request.FILES['profile_photo']
        user.save()
        profile.save()
    context_dict={}
    if profile.picture is not None:
        context_dict['picture'] = profile.picture
    else:
        context_dict['picture'] = ""
    return render(request, 'inspeakers/myaccount.html',context_dict)
# at the moment, review is part of the speaker profile page
# we can't control "login required" with this method
# possibly open a new page to add a review?
@login_required
def my_favourite(request,user_slug):
    return render(request, 'inspeakers/myfavourite.html')
@login_required
def add_review(request):
    return
@login_required
def user_logout(request):
    return

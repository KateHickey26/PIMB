from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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
    return render(request, 'inspeakers/signup.html')
def user_login(request):
    return render(request, 'inspeakers/login.html')
@login_required
def my_account(request):
    return render(request, 'inspeakers/myaccount.html')
# at the moment, review is part of the speaker profile page
# we can't control "login required" with this method
# possibly open a new page to add a review?
@login_required
def add_review(request):
    return
@login_required
def user_logout(request):
    return

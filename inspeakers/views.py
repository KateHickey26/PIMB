from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from inspeakers.models import *
from datetime import datetime

# Create your views here.
def home(request):
    context_dict = get_speakers(request, 'name', None)
    context_dict['page']['url'] = 'home'
    context_dict['description'] = 'Homepage'
    return render(request, 'inspeakers/home.html', context_dict)

def rate(request):
    context_dict = get_speakers(request, '-rate', None)
    context_dict['page']['url'] = 'home/rate'
    context_dict['description'] = 'Top Rated'
    return render(request, 'inspeakers/home.html', context_dict)

def tag(request, tag_name_slug):
    context_dict = get_speakers(request, 'name', tag_name_slug)
    context_dict['page']['url'] = 'home/tag/'+tag_name_slug
    context_dict['description'] = 'Tag: ' + tag_name_slug
    return render(request, 'inspeakers/home.html', context_dict)

def mfav(request):
    context_dict = get_speakers(request, '-favcount', None)
    context_dict['page']['url'] = 'home/fav'
    context_dict['description'] = 'Most Liked'
    return render(request, 'inspeakers/home.html', context_dict)


def get_speakers(request, order, tag, user = None):
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

    if user is not None:
        try:
            speakers = []
            sp = Favourite.objects.filter(user=user)
            for s in sp:
                speakers.append(s.speakers)
        except:
            speakers = []
    elif tag is None:
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
@login_required
def speakerprofileedit(request):
    if request.method == 'POST':
        description = request.POST.get('about')
        company = request.POST.get('company')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        experience = request.POST.get('experience')
        hourlyrate = request.POST.get('hourlyrate')
        youtube = request.POST.get('youtube')
        twitter = request.POST.get('twitter')
        ins = request.POST.get('ins')
        website = request.POST.get('website')
        tags = request.POST.get('tags')
        profile = SpeakerProfile.objects.get(speaker=request.user)
        profile.description = description
        profile.company = company
        profile.email = email
        profile.phone= phone
        profile.experience = experience
        profile.hourlyrate = hourlyrate
        profile.youtube = youtube
        profile.twitter = twitter
        profile.ins = ins
        profile.website = website
        tags = tags.split(';')
        for t in tags:
            o = Tag.objects.get_or_create(name=t)[0]
            profile.tags.add(o)
        profile.save()
    else:
        profile = SpeakerProfile.objects.get(speaker=request.user)
    context={}
    context['speaker'] = profile
    s = ""
    for t in profile.tags.all():
        s += t.name
    context['tags'] = s
    return render(request,'inspeakers/edit.html',context)

def speakerprofile(request, speaker_profile_slug):
    fav = request.GET.get('fav')
    user = request.user
    s = SpeakerProfile.objects.get(slug=speaker_profile_slug)
    context_dict={}
    if user.is_authenticated :
        profile = SpeakerProfile.objects.get(speaker=user)
        if fav == '0':
            Favourite.objects.filter(user=user).filter(speakers=s).delete()
        elif fav == '1':
            f = Favourite.objects.get_or_create(user=user,speakers=s)[0]
            f.save()

        if Favourite.objects.filter(user=user).filter(speakers=s).exists():
            context_dict['fav'] = True
        else:
            context_dict['fav'] = False
        s.favcount = Favourite.objects.filter(speakers=s).count()
        print(s.favcount)
        s.save()
        if request.method == 'POST':
            if 'profile_photo' in request.FILES:
                profile.picture = request.FILES['profile_photo']
            profile.save()
        user.save()
    else:
        context_dict['fav'] = None
    context_dict['speaker'] = s
    return render(request,'inspeakers/speakerprofile.html',context_dict)

@login_required
def comment(request,speaker_profile_slug):
    # Comment posted
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        time = str(datetime.now())[0:10]
        user = UserProfile.objects.get(user=request.user)
        speaker = SpeakerProfile.objects.get(slug=speaker_profile_slug)
        Comment.objects.create(user=user, body=comment_text, date=time, speaker=speaker)
    return HttpResponse("Success Comment")

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
            profile.profile_image = request.FILES['profile_photo']
        user.save()
        profile.save()
    context_dict={}
    if profile.profile_image is not None:
        context_dict['picture'] = profile.profile_image
    else:
        context_dict['picture'] = ""
    return render(request, 'inspeakers/myaccount.html',context_dict)
# at the moment, review is part of the speaker profile page
# we can't control "login required" with this method
# possibly open a new page to add a review?
@login_required
def my_favourite(request):
    context_dict = get_speakers(request,None,None,request.user)
    context_dict['page']['url'] = 'home'
    context_dict['description'] = 'My favourite'
    return render(request, 'inspeakers/home.html', context_dict)

@login_required
def my_reviews(request):
    return render(request,'inspeakers/myreviews.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('inspeakers:home'))

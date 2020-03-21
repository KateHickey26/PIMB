from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from inspeakers.models import *

# Create your views here.
def home(request):
    page = request.GET.get('page')
    max_result = request.GET.get('max_result')
    order = request.GET.get('order')
    tag = request.GET.get('tag')
    if max_result is None:
        max_result = 3
    if page is None:
        page = 1
    if order is None:
        order='name'
    context_dict = {}
    context_dict['speakers'] = get_speakers(max_result,page,order,tag)['speakers']
    return render(request,'inspeakers/home.html',context_dict)


def get_speakers(max_result, page, order, tag):
    if tag is None:
        return {'speakers': SpeakerProfile.objects.order_by(order)[(page-1)*max_result: (page)*max_result]}
    else:
        t = Tag.objects.get(name=tag)
        return {'speakers': SpeakerProfile.objects.filter(tags=t).order_by(order)[(page - 1) * max_result: (page) * max_result]}

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

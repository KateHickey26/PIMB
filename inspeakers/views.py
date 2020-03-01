from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'inspeakers/home.html')

def speakerprofile(request):
    return render(request,'inspeakers/speakerprofile.html')
def sign_up(request):
    return
def user_login(request):
    return
@login_required
def my_account(request):
    return
# at the moment, review is part of the speaker profile page
# we can't control "login required" with this method
# possibly open a new page to add a review?
@login_required
def add_review(request):
    return
@login_required
def user_logout(request):
    return
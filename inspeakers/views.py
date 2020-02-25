from django.shortcuts import render

# Create your views here.
def home(request):

def speakerprofile(request):

def sign_up(request):

def user_login(request):

@login_required
def my_account(request):

# at the moment, review is part of the speaker profile page
# we can't control "login required" with this method
# possibly open a new page to add a review?
@login_required
def add_review(request):

@login_required
def user_logout(request):

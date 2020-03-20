from django.urls import path
from inspeakers import views

# app_name = ' '

# the urls below will follow the app name above
urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/speakerprofile/', views.speakerprofile, name='speaker_profile'),
    path('/', views.post_detail, name='post_detail')
    path('signup/', views.sign_up, name='sign_up'),
    path('login/myaccount/', views.my_account, name='my_account'),
    # if we decide to have a new page to add a review
    path('home/speakerprofile/addreview/', views.add_review, name='add_review'),
]

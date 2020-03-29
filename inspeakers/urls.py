from django.urls import path
from inspeakers import views

app_name = 'inspeakers'

# the urls below will follow the app name above
urlpatterns = [
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('home/tag/<slug:tag_name_slug>/', views.tag, name='tag'),
    path('home/rate/', views.rate, name='rate'),
    path('home/fav/', views.mfav, name='fav'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('home/speakerprofile/<slug:speaker_profile_slug>', views.speakerprofile, name='speaker_profile'),
    path('home/speakerprofile/<slug:speaker_profile_slug>/comment', views.comment, name='comment'),
    path('home/speakerprofile', views.speakerprofileedit, name='speaker_profile_edit'),
    #path('/', views.post_detail, name='post_detail')
    path('signup/', views.sign_up, name='sign_up'),
    path('myaccount/', views.my_account, name='my_account'),
    path('myfavourite/', views.my_favourite, name='my_favourite'),
    path('myreviews/', views.my_reviews, name='my_reviews'),
]

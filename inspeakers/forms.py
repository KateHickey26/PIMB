from django import forms
from inspeakers.models import Comment
from inspeakers.models import SpeakerProfile
from inspeakers.models import UserProfile
from datetime import datetime, date


# forms for user login, signup, and profile?

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class SpeakerProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('website', 'picture',)

class CommentForm(forms.ModelForm):
    date = forms.DateField(widget=forms.HiddenInput(), initial = date.today,required=False)
    rating = forms.IntegerField(widget=forms.HiddenInput(), initial =0)
    content = forms.TextInput()

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

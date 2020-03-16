from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class SpeakerProfile(models.Model):
    speaker = models.OneToOneField(User, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True,max_length=20)

    tags = models.ManyToManyField("Tag")

    def __str__(self):
        return self.speaker.username

class Tag(models.Model):
    name = models.CharField(max_length=20)
    popularity = models.IntegerField(default=0)
    def __str__(self):
        return self.tag
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

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False) #to prevent spam, and manually allow comments, set to false

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Tag(models.Model):
    name = models.CharField(max_length=20)
    popularity = models.IntegerField(default=0)
    def __str__(self):
        return self.tag

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
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
    name = models.CharField(blank=True, max_length=30)
    description = models.CharField(blank=True, max_length=200)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True,max_length=20)
    rate = models.IntegerField(default=0)
    tags = models.ManyToManyField("Tag")
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(SpeakerProfile, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = 'speakerprofiles'

    def __str__(self):
        return self.speaker.username


class Comment(models.Model):
    post = models.ForeignKey(SpeakerProfile,on_delete=models.CASCADE,related_name='comments')
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



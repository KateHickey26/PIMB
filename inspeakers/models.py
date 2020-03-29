from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify
# Create your models here.
class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    profile_image = models.ImageField(upload_to='profile_images', blank=True)

    favs = models.ManyToManyField("SpeakerProfile")

    def __str__(self):
        return self.user.username

class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    speakers = models.ForeignKey("SpeakerProfile", on_delete=models.CASCADE)

class SpeakerProfile(models.Model):
    speaker = models.OneToOneField(User, on_delete=models.CASCADE)
    favcount = models.IntegerField(default=0)
    website = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    twitter = models.URLField(blank=True)
    ins = models.URLField(blank=True)
    name = models.CharField(blank=True, max_length=30)
    description = models.CharField(blank=True, max_length=200)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    company = models.CharField(blank=True,max_length=100)
    experience = models.CharField(blank=True,max_length=20)
    hourlyrate = models.CharField(blank=True,max_length=20)
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
    user = models.ForeignKey('UserProfile', on_delete=models.CASCADE, related_name='comments',blank=True)
    speaker = models.ForeignKey('SpeakerProfile', on_delete=models.CASCADE, related_name='comments',blank=True)
    date = models.DateField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)
    body = models.TextField(blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    #active = models.BooleanField(default=False) #to prevent spam, and manually allow comments, set to false


    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)

class Tag(models.Model):
    name = models.CharField(max_length=20)
    popularity = models.IntegerField(default=0)
    slug = models.SlugField(blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tag, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = 'tags'

    def __str__(self):
        return self.name

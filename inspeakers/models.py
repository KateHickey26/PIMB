from django.db import models

# Create your models here.
class UserProfile(models.Model):
    # Links UserProfile to a User model instance.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # The additional attributes we wish to include.
    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username

class SpeakerProfile(models.Model):
    speaker = models.OneToOneField(Speaker, on_delete=models.CASCADE)

    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    email = models.EmailField(blank=True)
    phone = models.PhoneField(blank=True)

    def __str__(self):
        return self.speaker.username

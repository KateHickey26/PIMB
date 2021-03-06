from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import SpeakerProfile, Comment
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'post', 'created_on', 'active')
    list_filter = ('active', 'created_on')
    search_fields = ('name', 'email', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(active=True)
        # actions method. Allows us to approve many comments at once
        # creating a super user and logging in should show the comments model.

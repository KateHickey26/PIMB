from django import template
from inspeakers.models import *

register = template.Library()

@register.inclusion_tag('inspeakers/tags.html')
def get_tags(speaker=None):
    if speaker is not None:
        tags = speaker.tags.all()
    else:
        tags = Tag.objects.order_by('popularity')
    return {'tags': tags}

@register.inclusion_tag('inspeakers/review.html')
def get_reviews(speaker=None):
    if speaker is not None:
        comments = Comment.objects.filter(speaker=speaker).order_by('-created_on')[0:5]
    return {'comments': comments}

@register.inclusion_tag('inspeakers/review.html')
def my_reviews(user=None):
    if user is not None:
        up = UserProfile.objects.get(user=user)
        comments = Comment.objects.filter(user=up)
    return {'comments': comments}


from django import template
from inspeakers.models import Tag,SpeakerProfile

register = template.Library()

@register.inclusion_tag('inspeakers/tags.html')
def get_tags():
    return {'tags': Tag.objects.order_by('popularity')}

@register.inclusion_tag('inspeakers/cards.html')
def get_speakers(num=3):
    return {'speakers': SpeakerProfile.objects.order_by('rate')[0:num]}
from django import template
from inspeakers.models import Tag,SpeakerProfile

register = template.Library()

@register.inclusion_tag('inspeakers/tags.html')
def get_tags(speaker=None):
    if speaker is not None:
        tags = speaker.tags.all()
    else:
        tags = Tag.objects.order_by('popularity')
    return {'tags': tags}

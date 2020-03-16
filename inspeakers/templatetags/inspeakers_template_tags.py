from django import template
from inspeakers.models import Tag

register = template.Library()

@register.inclusion_tag('inspeakers/tags.html')
def get_tags():
    return {'tags': Tag.objects.order_by('popularity')}
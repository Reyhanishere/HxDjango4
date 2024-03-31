from django import template
from django.template.defaultfilters import stringfilter

import markdown as md

register = template.Library()

@register.filter
def model_type(obj):
    return obj.__class__.__name__

@register.filter()
@stringfilter
def markdown(value):
    return md.markdown(value, extensions=['markdown.extensions.fenced_code',
                                          'footnotes',
                                          'tables',
                                          'toc'])
from django import template

register = template.Library()

@register.filter
def model_type(obj):
    return obj.__class__.__name__
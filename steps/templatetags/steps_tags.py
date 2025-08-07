import random
import re

from django import template

from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def wModel(value):
    return value._meta.model_name

@register.filter
def isModel(value, arg):
    return value._meta.model_name == arg.lower()

@register.filter
def shuffleDict(arg):
    if isinstance(arg, dict):
        items = list(arg.items())
        random.shuffle(items)
        return items
    return arg

@register.filter(name='sep_paraph')
def sep_paraph(value):
    if not value:
        return ''
    
    paras = re.split(r'\n{1,}', str(value))
    paras = [f'<p dir="auto">{p.strip()}</p>' for p in paras if p.strip()]

    return mark_safe('\n'.join(paras))

@register.filter
def classname(obj, class_name):
    return obj.__class__.__name__== class_name

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

import markdown as md
import re

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

@register.filter(name='emphasize')
def emphasize(value):
    try:
        lined = value.split("\n")
        all_lines = []
        for i in lined:
            if len(i)>2 and i[0:2]=="• ":
                new_line = f"<p class='ros-phe-ttl-ppr'>{i[2:]}</p>"
                all_lines.append(new_line)
            elif len(i)>2 and i[-2] == "*":  # Add a check to ensure the line is not empty
                new_line = f"<span class='red-txt-ros-phe'>{i[:-2]}</span><br/>"
                all_lines.append(new_line)
            elif len(i)>2 and i[-1] == "*":  # Add a check to ensure the line is not empty
                new_line = f"<span style='color:#d22; font-weight: bold'>{i[:-1]}</span><br/>"
                all_lines.append(new_line)
            elif list(i).count('-')>3 :
                all_lines.append('<hr/>')
            elif len(i)<3:
                pass
            else:
                all_lines.append(f"{i}<br/>")
        final = "".join(all_lines)
        return final
    except:
        return None

@register.filter(name='sep_paraph')
def sep_paraph(value):
    if not value:
        return ''
    paras = re.split(r'\n{1,}', str(value))
    paras = [f'<p dir="auto" style="margin-bottom: 0.5rem;">{p.strip()}</p>' for p in paras if p.strip()]
    return mark_safe('\n'.join(paras))

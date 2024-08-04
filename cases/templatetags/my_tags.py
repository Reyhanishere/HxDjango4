from django import template

register = template.Library()

@register.filter(name='emphasize')
def emphasize(value):
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

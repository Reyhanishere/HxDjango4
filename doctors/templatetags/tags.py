import jdatetime
from django import template

register = template.Library()

def gregorian_to_jalali(date):

    gy, gm, gd = date.split(" ")
    gy, gm, gd = int(gy), int(gm), int(gd)

    g_d_m = [0, 31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334]
    if gm > 2:
        gy2 = gy + 1
    else:
        gy2 = gy
    days = 355666 + (365 * gy) + ((gy2 + 3) // 4) - ((gy2 + 99) // 100) + ((gy2 + 399) // 400) + gd + g_d_m[gm - 1]
    jy = -1595 + (33 * (days // 12053))
    days %= 12053
    jy += 4 * (days // 1461)
    days %= 1461
    if days > 365:
        jy += (days - 1) // 365
        days = (days - 1) % 365
    if days < 186:
        jm = 1 + (days // 31)
        jd = 1 + (days % 31)
    else:
        jm = 7 + ((days - 186) // 30)
        jd = 1 + ((days - 186) % 30)
    return (str(jy), jm, jd)


def month_name(month):
    months_names_list=['ماه‌ها','فروردین','اردیبهشت','خرداد','تیر','مرداد','شهریور','مهر','آبان','آذر','دی','بهمن','اسفند']
    return months_names_list[month]

@register.filter
def to_jalali(value, arg):
    month_format, year_format = arg.split(', ')
    if not value:
        return ''
    # if type(value) == 'str':
    jalali_date = gregorian_to_jalali(value)
    if year_format == 'long':
        year = jalali_date[0]
    else:
        year = jalali_date[0][2:]

    if month_format == 'name':
        month = month_name(jalali_date[1])
        return f"{jalali_date[0][2:]} {month} {year}"

    else: 
        return f"{jalali_date[0][2:]}/{jalali_date[1]:02d}/{jalali_date[2]:02d}"

@register.filter
def j_date(value, arg):
    j_date = jdatetime.date.fromgregorian(date=value)
    string_date = str(j_date)
    # return string_date
    year, month, day = string_date.split('-')
    month_format, year_format = arg.split(', ')

    if not value:
        return ''
    # if type(value) == 'str':
    if year_format != 'long':
        year = year[2:]
    
    output = f"{year}/{month}/{day}"

    if month_format == 'name':
        month = month_name(int(month))
        output = f"{day} {month} {year}"

    return output

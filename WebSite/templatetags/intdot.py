import re
from django.db import connection
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.encoding import force_text
# from WebSite.models import TranslateModel
from django.utils import translation
import jdatetime

register = template.Library()

@register.filter
def intdot(value):
    orig = force_text(value)
    new = re.sub("^(-?\d+)(\d{3})", '\g<1>,\g<2>', orig)
    if orig == new:
        return new
    else:
        return intdot(new)


@register.filter
def StatusName(value):
    if value == 0 :
        return 'پیش نویس'
    elif value == 1 :
        return 'ارسال شده'
    elif value == 2 :
        return 'تایید شده'
    elif value == 3 :
        return 'تایید نشده'
    return value



def convertdate(year, month, day, type):
    if type.lower() == 'shamsitomiladi':
        res = jdatetime.date(year, month, day).togregorian()
    elif type.lower() == 'miladitoshamsi':
        res = jdatetime.date.fromgregorian(day=day, month=month, year=year)
    return res


@register.filter
def MiladiToShamsi(Date, request):
    Date_split = Date.split('/')
    year = Date_split[0]
    month = Date_split[1]
    day = Date_split[2]
    type = 'MiladiToShamsi'
    t = convertdate(int(year), int(month), int(day), type)
    return t


@register.filter
def ShamsiToMiladi(Date, request):
    Date_split = Date.split('/')
    year = Date_split[0]
    month = Date_split[1]
    day = Date_split[2]
    type = 'ShamsiToMiladi'
    t = convertdate(int(year), int(month), int(day), type)
    return t

@register.filter
def urlreplace(value):
    url = str(value)
    new = url.replace(' ','-')
    return new
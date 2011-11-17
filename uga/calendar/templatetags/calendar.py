from django import template
import re


register = template.Library()

def calendar_month_url(path, year, month):
    if re.match(r'.*\d{4}/\d{2}/$', path):
        path = '/'.join(path.split('/')[:-3])

    path = path.rstrip('/')

    return '%s/%d/%02d/' % (path, year, month)

register.simple_tag(calendar_month_url)

"""
Based on http://djangosnippets.org/snippets/1494/
"""

import urllib
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter
@stringfilter
def qrcode_url(value, size='150x150'):
    """
    Generate QR Code image from a string with the Google charts API

    http://code.google.com/intl/fr-FR/apis/chart/types.html#qrcodes

    Exemple usage --
    {{ my_string|qrcode:'150x150' }}

    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """

    width, height = size.split('x')
    width, height = int(width), int(height)
    base = 'http://chart.apis.google.com/chart'
    value = conditional_escape(value)
    query = urllib.urlencode({
        'chs': '{}x{}'.format(width, height),
        'cht': 'qr',
        'chl': value,
        'choe': 'UTF-8',
        'chld': 'm|0'
    })
    return mark_safe('{}?{}'.format(base, query))


@register.filter
@stringfilter
def qrcode(value, size='150x150'):
    """
    Generate QR Code image from a string with the Google charts API

    http://code.google.com/intl/fr-FR/apis/chart/types.html#qrcodes

    Exemple usage --
    {{ my_string|qrcode:'150x150' }}

    <img src="http://chart.apis.google.com/chart?chs=150x150&amp;cht=qr&amp;chl=my_string&amp;choe=UTF-8" alt="my alt" />
    """

    width, height = size.split('x')
    width, height = int(width), int(height)
    url = qrcode_url(value, size)
    alt = conditional_escape(value)

    return mark_safe(u'<img class="qrcode" src="{}" width="{}" height="{}" alt="{}" />'.format(url, width, height, alt))

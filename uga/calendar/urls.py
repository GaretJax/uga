from django.conf.urls.defaults import *

urlpatterns = patterns('uga.calendar.views',
    url(r'^(?P<year>\d{4})/(?P<month>\w{2})/$', 'month', name='single_month'),
    url(r'^$', 'month', name='current_month'),
)

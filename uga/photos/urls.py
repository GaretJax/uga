from django.conf.urls.defaults import *

urlpatterns = patterns('uga.photos.views',
    #url(r'^(?P<year>\d{4})/(?P<month>\w{2})/$', 'month', name='single_month'),
    url(r'^$', 'albums', name='albums-list'),
)


from django.conf.urls.defaults import *

urlpatterns = patterns('uga.inscriptions.views',
    url(r'^$', 'list_events', name='inscriptions.list'),
    url(r'^iscrizione/(?P<list_id>\d+)/$', 'subscribe', name='inscriptions.subscribe'),
    url(r'^gestisci/(?P<inscription_id>\d+)/(?P<auth>[^/]+)/$', 'manage', name='inscriptions.manage'),
    url(r'^gestisci/(?P<inscription_id>\d+)/(?P<auth>[^/]+)/rimuovi/(?P<name_id>\d+)/$', 'remove', name='inscriptions.remove'),
)

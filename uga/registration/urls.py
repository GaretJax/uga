from django.conf.urls.defaults import *

urlpatterns = patterns('uga.registration.views',
    url(r'^iscrivi/$', 'enroll', name='enroll'),
    url(r'^esporta-email/$', 'export_emails', name='export_emails'),
    url(r'^$', 'list', name='list'),
)
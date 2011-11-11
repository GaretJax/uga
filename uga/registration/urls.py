from django.conf.urls.defaults import *

urlpatterns = patterns('uga.registration.views',
    url(r'^iscrivi/$', 'enroll', name='enroll'),
    url(r'^modifica/(?P<member_id>\d+)/$', 'edit', name='edit_member'),
    url(r'^modifica/(?P<member_id>\d+)/iscrizioni/$', 'subscriptions', name='edit_subscriptions'),
    url(r'^modifica/(?P<member_id>\d+)/mailing-list/$', 'mailing_list', name='edit_mailing_list'),
    url(r'^modifica/(?P<member_id>\d+)/rimuovi/$', 'remove', name='remove_member'),
    url(r'^esporta-email/$', 'export_emails', name='export_emails'),
    url(r'^$', 'list', name='list'),
)

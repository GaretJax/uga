from django.conf.urls.defaults import *

urlpatterns = patterns('uga.registration.views',
    url(r'^iscrivi/$', 'enroll', name='enroll'),
    url(r'^modifica/(?P<member_id>\d+)/$', 'edit', name='edit_member'),
    url(r'^modifica/(?P<member_id>\d+)/iscrizioni/$', 'subscriptions', name='edit_subscriptions'),
    url(r'^modifica/(?P<member_id>\d+)/mailing-list/$', 'mailing_list', name='edit_mailing_list'),
    url(r'^modifica/(?P<member_id>\d+)/rimuovi/$', 'remove', name='remove_member'),
    url(r'^rinnova/(?P<random_id>\w+).png$', 'renew_qrcode', name='renew_qrcode'),
    url(r'^esporta-dati/$', 'export_data', name='export_data'),
    url(r'^esporta-dati/soci.xls$', 'export_excel', name='export_excel'),
    url(r'^$', 'list', name='list'),
)

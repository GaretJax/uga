from django.conf.urls.defaults import *

urlpatterns = patterns('uga.registration.views',
    url(r'^iscrivi/$', 'enroll', name='enroll'),
    url(r'^$', 'list', name='list'),
)
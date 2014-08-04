from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^$', 'uga.registration.views.announce', name='announce'),
    url(r'^grazie/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'uga/registration/announce-ok.html',
    }, name='announce-ok'),
)

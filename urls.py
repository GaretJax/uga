from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.views.generic.simple import redirect_to

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/logs/', include('sentry.web.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('uga.auth.urls', namespace='auth')),
    url(r'^preview/$',redirect_to, {'url': '/', 'permanent': False}),
    url(r'^', include('cms.urls')),
)

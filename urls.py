from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/logs/', include('sentry.web.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('uga.auth.urls', namespace='auth')),
    url(r'^', include('cms.urls')),
)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    import os
    urlpatterns += patterns('',
        url(r'^media/admin/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': os.path.join(os.path.dirname(admin.__file__), 'media'),
        }),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^' + settings.MEDIA_URL.lstrip('/'), include('appmedia.urls')),
   )


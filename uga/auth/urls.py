from django.conf.urls.defaults import *

urlpatterns = patterns('',
    url(r'^accedi/$', 'django.contrib.auth.views.login',
            {'template_name': 'auth/login.html'}, name='login'),
    url(r'^esci/$', 'django.contrib.auth.views.logout',
            {'next_page': '/'}, name='logout'),
)

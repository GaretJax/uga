# Django settings for project project.

import os

PROJECT_BASE = os.path.dirname(os.path.dirname(__file__))

gettext = lambda s: s

ADMINS = []

INTERNAL_IPS = ('127.0.0.1',)

PORT = 8000

SEND_BROKEN_LINK_EMAILS = True

IGNORABLE_404_ENDS = [
    'favicon.ico',
    'favicon.ico/',
    'favicon.png',
    'crossdomain.xml',
    'crossdomain.xml/',
    'robots.txt',
    'robots.txt/',
]

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'sqlite3',
        'NAME': os.path.join(PROJECT_BASE, 'assets', 'database.sqlite'),
        'USER': '',             # Not used with sqlite3.
        'PASSWORD': '',         # Not used with sqlite3.
        'HOST': '',             # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',             # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Zurich'

#import warnings
#warnings.filterwarnings(
#        'error', r"DateTimeField received a naive datetime",
#        RuntimeWarning, r'django\.db\.models\.fields')

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'it-it'

LANGUAGES = [
    ('it', 'Italiano'),
]

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

USE_TZ = False

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_BASE, 'media')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/media/'

STATICFILES_DIRS = (
    os.path.join(PROJECT_BASE, 'static'),
)
STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_BASE, 'collected-static')

# List of callables that know how to import templates from various sources.
JINJA2_TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_LOADERS = (
    'coffin.template.loaders.Loader',
)

#TEMPLATE_LOADERS = JINJA2_TEMPLATE_LOADERS

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    'django.contrib.messages.context_processors.messages',
    'cms.context_processors.media',
    'sekizai.context_processors.sekizai',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
)

#AUTH_PROFILE_MODULE = 'auth.UserProfile'

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

LOGIN_URL = '/accedi/'
LOGIN_REDIRECT_URL = '/'
#PERMISSIONS_VIEW = 'adb.frontend.auth.views.permission_required'

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_BASE, 'templates'),
)

INSTALLED_APPS = (
    # Django apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #'django.contrib.gis',

    # Third party apps
    'sentry',
    'sentry.client',
    'sentry.plugins.sentry_urls',
    'schedule',
    #'mailchimp',
    #'haystack',
    'south',
    'reversion',
    'coffin',

    # Django cms apps
    'cms',
    'mptt',
    'menus',
    'sekizai',
    'appmedia',
    'cms.plugins.text',
    'cms.plugins.picture',
    'cms.plugins.link',
    'cms.plugins.file',
    'cms.plugins.snippet',
    'cms.plugins.googlemap',
    'cms.plugins.flash',
    'cms.plugins.teaser',
    'cms.plugins.video',
    'cms.plugins.twitter',

    # Blog
    'cmsplugin_blog',
    'djangocms_utils',
    'simple_translation',
    'tagging',
    #'missing',

    # UGA Apps
    'uga.registration',
    'uga.calendar',
    'uga.photos',
    'uga.auth',
    'uga.inscriptions',
    'uga.locations',
)

JINJA2_DISABLED_TEMPLATES = (
    r'[^/]+\.html',
    r'uga/(registration|calendar|photos)',
    r'inscriptions/(?!mails)',
    r'(cms|menu|auth|admin|admin_doc|registration)/',
    r'(cmsplugin_blog|simple_translation)/',
)


CMS_TEMPLATES = (
    ('index.html', 'Homepage template'),
    ('admin.html', 'Admin template'),
    ('left-sidebar.html', 'Normal page (left sidebar)'),
)

CMS_SHOW_END_DATE = True
CMS_SHOW_START_DATE = True
CMS_URL_OVERWRITE = True
CMS_MENU_TITLE_OVERWRITE = True
CMS_REDIRECTS = True
CMS_SEO_FIELDS = True

CMS_HIDE_UNTRANSLATED = False
CMS_LANGUAGE_FALLBACK = True

#CMS_PAGE_MEDIA_PATH = 'assets/cms/'
#CMS_MEDIA_ROOT = os.path.join(os.path.dirname(cms.__file__), 'media', 'cms') + '/'
CMS_PERMISSION = True
CMS_SOFTROOT = True
CMS_MODERATOR = False
CMS_CONTENT_CACHE_DURATION = 1

# Django-schedule configuration
FIRST_DAY_OF_WEEK = 1 # Monday

# Django-schedule configuration
FIRST_DAY_OF_WEEK = 1


#HAYSTACK_SITECONF = 'adb.frontend.search_sites'
#HAYSTACK_SEARCH_ENGINE = 'solr'
#HAYSTACK_SEARCH_ENGINE = 'simple'
#HAYSTACK_SOLR_URL = 'http://127.0.0.1:8983/solr'


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}


MAILCHIMP_API_KEY = ''
MAILING_LIST_ID = ''

PICASA_USER = 'ugawebmail@gmail.com'

# TODO: replace with local verions
JQUERY_JS = 'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js'
JQUERY_UI_JS = 'https://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/jquery-ui.min.js'
JQUERY_UI_CSS = 'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.12/themes/smoothness/jquery-ui.css'

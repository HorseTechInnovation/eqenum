"""
Django settings for ktotback project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import markdown


mode = "PRODUCTION"
SITE_ID = 1
SITE_URL = "http://dressagecalculator.com"
SITE_NAME = "Reference Data for Horses"

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


VERSION = "0.01 Jan2019"

SECRET_KEY = 'kuu98^yGGf$)ooooovjf8&uztcdn'


DEBUG = False



ALLOWED_HOSTS = ['www.dressagecalculator.com','dressagecalculator.com', 'dc.iofh.io', 'skor.ie', 'www.skor.ie']

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    "django.contrib.auth.backends.ModelBackend",

    # `allauth` specific authentication methods, such as login by e-mail
    "allauth.account.auth_backends.AuthenticationBackend",

)

AUTH_USER_MODEL = "web.CustomUser"
ACCOUNT_USER_MODEL_USERNAME_FIELD = "email"
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'


POST_OFFICE = {
    'DEFAULT_PRIORITY': 'now',
    'LOG_LEVEL': 2,
}
# Application definition


MIDDLEWARE = [
    # Media middleware has to come first
    #'mediagenerator.middleware.MediaMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'simple_history.middleware.HistoryRequestMiddleware',
    'web.middleware.XsSharing',
    'django_user_agents.middleware.UserAgentMiddleware',
    #'web.middleware.EveryoneIsUser',
]


INSTALLED_APPS = [

    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.humanize',

    'countries_plus',
    'languages_plus',
    'django_nose',

    "post_office",
    'django_filters',
    'rest_framework',
    'web',
    'treebeard',
    'markupfield',

    'django_js_error_hook',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',

    # 'camera_imagefield',

    'import_export',


]

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'



# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

MARKUP_FIELD_TYPES = (
    ('markdown', markdown.markdown),

)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-GB'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

AUTH_USER_MODEL = 'web.CustomUser'
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"
APPEND_SLASH = True


ADMINS = [('Phoebe','phoebebright310@gmail.com'),('Phoebe','phoebe@horsetech.ie'), ('System','calculator@horsetech.ie')]
DEFAULT_FROM_EMAIL = "DressageCalculator.com <info@dressagecalculator.com>"
DEFAULT_TO_EMAIL = "info@dressagecalculator.com"
NOTIFY_NEW_USER_EMAILS = "phoebebright310@gmail.com"

EMAIL_BACKEND = 'post_office.EmailBackend'



# Static files (CSS, JavaScript, Images)

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'compressor.finders.CompressorFinder',
)

STATIC_ROOT = os.path.join(BASE_DIR, 'shared_static')
STATIC_URL = '/shared_static/'

# compress both js and css - settings for django-compressor
# COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.SlimItFilter',]
# COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSCompressorFilter',]
# COMPRESS_OFFLINE = False
# COMPRESS_ENABLED = True

# Absolute path to the directory that holds media.
MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')
MEDIA_URL = '/uploads/'


ASSETS_ROOT = os.path.join(BASE_DIR, 'assets')
ASSETS_URL = '/assets/'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),

                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': False,
            'context_processors': [

                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                # "allauth.account.context_processors.account",
                # "allauth.socialaccount.context_processors.socialaccount",
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]


# ALLAUTH settings


SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'https'},
        #'AUTH_PARAMS': {'auth_type': 'reauthenticate'},  this will require people re-enter their password in facebook
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        # 'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12',
    }
}

SOCIALACCOUNT_ADAPTER = 'web.views.DCSocialAccountAdapter'

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"
DEFAULT_HTTP_PROTOCOL = "https"
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"   # currently using custom signup if not facebook


# TEMPLATE_CONTEXT_PROCESSORS = TEMPLATES[0]['OPTIONS']['context_processors']   # keeps allauth happy

# Registration settings
# REGISTRATION_AUTO_LOGIN = True
# ACCOUNT_ACTIVATION_DAYS = 7

API = "api/v1/"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        #'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),

}

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s  %(message)s'
        },
        "post_office": {
            "format": "[%(levelname)s]%(asctime)s PID %(process)d: %(message)s",
            "datefmt": "%d-%m-%Y %H:%M",
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'logfile': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, "logs/django.log"),
            'formatter': 'standard',
        },
        'contactlog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, "logs/contact.log"),
            'formatter': 'standard',
        },
        'email': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, "logs/email.log"),
            'formatter': 'standard',
        },
        'jobslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'filename': os.path.join(BASE_DIR, "logs/jobs.log"),
            'formatter': 'standard',
        },
        "post_office": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "post_office"
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # everything that goes to syslog goes to papertrail https://papertrailapp.com/systems/1848252051/events
        'SysLog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'formatter': 'standard',
            'address': ('logs6.papertrailapp.com', 34636)
        },
    },
    'loggers': {
        'django': {
            'handlers': ['logfile','console','SysLog'],
            'level': 'INFO',
            'propagate': True,
        },
        'jobs': {
            'handlers': ['jobslog','console','SysLog'],
            'level': 'INFO',
            'propagate': True,
        },
        'contact': {
            'handlers': ['contactlog', ],
            'level': 'DEBUG',
            'propagate': True,
        },
        'email': {
            'handlers': ['email', ],
            'level': 'DEBUG',
            'propagate': True,
        },

        "post_office": {
            "handlers": ["post_office",],
            "level": "INFO"
        },

        'javascript_error': {
            'handlers': [ 'logfile','console','SysLog'],
            'level': 'ERROR',
            'propagate': True,
        },

    },
}


BOT_LIST = ['63.143.42.247','66.249.66.87']
try:

    localpath=os.path.join(BASE_DIR, 'config/settings_local.py')
    if  os.path.exists(localpath):
        with open(localpath) as f:
            code = compile(f.read(), localpath, 'exec')
            exec(code, globals(), locals())

except:
    pass
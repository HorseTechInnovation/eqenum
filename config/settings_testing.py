from .settings import *

ALLOWED_HOSTS = ['*', ]

#  OVerride settings

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

EMAIL_PORT = 1025
EMAIL_HOST = 'localhost'
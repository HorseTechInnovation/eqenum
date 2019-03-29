Setup new Environment
======================

Example local settings::

    DEBUG=True
    COMPRESS_ENABLED=False

    # INSTALLED_APPS += ('behave_django',)
    #INSTALLED_APPS.append('debug_toolbar',)
    #MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware',)
    DATABASES = {
        'default': {
            'ENGINE':  'django.db.backends.postgresql_psycopg2',
            'NAME': 'eqenum',
            'USER': '',
            'PASSWORD': '',
            'HOST': 'localhost',
            'PORT': '',

        },

    }

    WSGI_APPLICATION = None

    SITE_ID = 1
    SITE_URL = "http://127.0.0.1:8000"
    INTERNAL_IPS = "127.0.0.1"



    ALLOWED_HOSTS = ['*',]

    TEMPLATES[0]['OPTIONS']['debug'] =True

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }



    EMAIL_PORT = 1025
    EMAIL_HOST='localhost'


    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,

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
            "post_office": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "post_office"
            },
        },
        'loggers': {
            'django': {
                'handlers': ['logfile','console'],
                'level': 'DEBUG',
                'propagate': True,
            },
            'django.template': {
                'handlers': ['console'],
                'level': 'WARNING',
            },
            'django.db.backends': {
                'level': 'WARNING',
                'handlers': ['console'],
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

        },
    }

Need logs directory:

    mkdir logs

To populate countries and languages run::

    python manage.py update_countries_plus
    python manage.py loaddata languages_data.json.gz


Then to get culture codes use url (superuser only):

    /update_culture_codes/



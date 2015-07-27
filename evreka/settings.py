"""
Django settings for evreka project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from logging.handlers import SysLogHandler,SocketHandler,DEFAULT_TCP_LOGGING_PORT
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'e(+9#8i$^=_61$o=b#(!&+*4r^6(xq-8)@k55wsc7c=z%z^=f0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LANGUAGES = [
  ('tr', 'Turkish'),
  ('en', 'English'),
]

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'evrekaTest',
    'homepage',
    'bootstrap3',
    'news',
)
# RELATED TO NEWS APP
NEWS_NUM_RECENT = 10
NEWS_PAGE_SIZE = 10

NEWS_FEED_TITLE = 'Recent Articles'
NEWS_FEED_DESCRIPTION = 'Recent Articles'
NEWS_FEED_LINK = '/news/'

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'evrekaTest.middleware.RequestLoggingMiddleware',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '#[%(asctime)s]#%(levelname)s#%(message)s#',
             #'datefmt': '%s'
        },
        'simple': {
            'format': '## [%(asctime)s] [%(levelname)s]  %(module)s  %(name)s  %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'file': {           # ALL REQUESTS
            'class':'evrekaTest.loggers.CustomRotatingFileHandler',
            'filename': 'django_request.log',
            'maxBytes' : 1024*1024*1, # 1MB
            'backupCount' : 10,
            #'formatter':'standard',
        },
        'inputfile': {      # HARDWARE INPUT POST REQUESTS
            'class':'evrekaTest.loggers.CustomRotatingFileHandler',
            'filename': 'django_input.log',
            'maxBytes': 1024*1024*1, # 1MB
            'backupCount': 10,
            #'formatter': 'standard',
        },
        'db':{
            'level': 'WARNING',
            'class': 'evrekaTest.loggers.ReqDbLogHandler',
            'formatter': 'simple'
        }
    },
    'loggers': {
        'django.request': {
            'level': 'DEBUG',
            'propagate': True,
        },
        '': {               # EVERYTHING : RequestLogs, Error Logs, Warning Logs
            'handlers': ['db','file'],
            'level': 'INFO',
            'propagate': False,
        },
        'inputlogs': {      # HARDWARE INPUT LOGS
            'handlers': ['inputfile'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}

ROOT_URLCONF = 'evreka.urls'

WSGI_APPLICATION = 'evreka.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'tr-TR'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT =  os.path.join(BASE_DIR,  'media')

MEDIA_URL = '/media/'

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale/'),
)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR,  'templates'),
)

STATIC_ROOT = os.path.join(BASE_DIR,  'static')
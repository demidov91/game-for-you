"""
Django settings for game_for_everyone project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import logging
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'south',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    #'django.contrib.staticfiles',
    'relations',
    'core',
    'tournament',
    'custom_registration',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.facebook',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.contrib.messages.context_processors.messages",
    "django.core.context_processors.request",
    "allauth.account.context_processors.account",
    "allauth.socialaccount.context_processors.socialaccount",
    "core.middleware.locale.add_common_template_variables",
)

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

ROOT_URLCONF = 'core.urls'

#WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATETIME_FORMAT = 'j F o H:i'

DATETIME_INPUT_FORMATS = (
    '%d.%m.%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%d.%m.%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%d.%m.%Y %H:%M',        # '10/25/2006 14:30'
    '%d.%m.%Y',              # '10/25/2006'
    '%d.%m.%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%d.%m.%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%d.%m.%y %H:%M',        # '10/25/06 14:30'
    '%d.%m.%y',              # '10/25/06'
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'

)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
SITE_ID = 1
LOGIN_URL = '/?force-login'



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'app_static')
SERVE_STATIC = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_ON_GET = False
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION=True

LOGGING = {
    'version': 1,
    'handlers': {
        'common_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/debug.log'),
            'when': 'W0',
        },
        'common_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/warn.log'),
            'when': 'W0',
        },
        'common_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/info.log'),
            'when': 'W0',
        },
    },
    'loggers': {
        '': {
            'handlers': ['common_warning', 'common_info', 'common_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

SOUTH_TESTS_MIGRATE = False

try:    
    from core.local_settings import *
except ImportError:
    pass
 
LANGUAGES = (
    ('ru', _('Russian')),
    ('be', _('Belarussian')),
)
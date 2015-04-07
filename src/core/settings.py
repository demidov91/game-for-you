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
    'django.contrib.staticfiles',
    'relations',
    'core',
    'tournament',
    'chat',
    'custom_registration',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.vk',
    'allauth.socialaccount.providers.facebook',
    'compressor',
    'logicaldelete',
    'ckeditor',
    'django.contrib.flatpages',
    'django_mobile',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
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
    "core.middleware.core.add_common_template_variables",
    "django_mobile.context_processors.flavour",
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

LANGUAGE_CODE = 'ru'

USE_I18N = True

USE_L10N = False

USE_TZ = False

TIME_ZONE = 'Europe/Minsk'

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

SHORT_DATE_FORMAT = 'j.m.Y H:i'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = False
SITE_ID = 1
LOGIN_URL = '/?force-login'
ACCOUNT_EMAIL_VERIFICATION='optional'
ACCOUNT_LOGIN_AFTER_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = 'index'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_URL = '/'
STATIC_ROOT = os.path.join(BASE_DIR, 'app_static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'core', 'media')
MEDIA_URL = '/media/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'core', 'media'),
)
CKEDITOR_UPLOAD_PATH = 'user_uploads/'
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'Full',
        'height': 291,
        'width': 835,
    },
    'event': {
        'toolbar': 'Event',
        'height': 300,
        'width': '100%',
        'toolbar_Event': [
            ['Format', 'Font', 'FontSize', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'],
            ['NumberedList', 'BulletedList'],
            ['JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', ],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule', ],
            ['TextColor', 'BGColor', 'Smiley'],
        ],
        'removeDialogTabs': 'link:upload;link:advanced;image:Upload;image:Link;image:advanced',
        'resize_enabled': False,
        'customConfig': os.path.join(MEDIA_URL, 'js', 'ckeditor_config.js'),
    },
    'chat': {
        'toolbar': 'Chat',
        'height': 125,
        'width': '30em',
        'toolbar_Chat': [
            ['Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'],
            ['Link', 'Unlink'],
            ['Image', 'TextColor', 'BGColor', 'Smiley'],
        ],
        'removeDialogTabs': 'link:upload;link:advanced;image:Upload;image:Link;image:advanced',
        'resize_enabled': False,
        'customConfig': os.path.join(MEDIA_URL, 'js', 'ckeditor_config.js'),
    },
}

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    'compressor.finders.CompressorFinder',
)


GET_AUTH_PARAM = 'readpermission'
LOGIN_REDIRECT_URL = 'index'
LOGOUT_ON_GET = False

DEFAULT_TAGS = (1, )
SOUTH_TESTS_MIGRATE = False
# Id of the tag which chat should be displayed on the index page.
BASE_TAG = None

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d] %(message)s'
        },
    },
    
    'handlers': {
        'common_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/debug.log'),
            'when': 'W0',
            'formatter': 'verbose',
        },
        'common_warning': {
            'level': 'WARNING',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/warn.log'),
            'when': 'W0',
            'formatter': 'verbose',
        },
        'common_info': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/info.log'),
            'when': 'W0',
            'formatter': 'verbose',
        },
        'common_error': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, '..', 'logs/error.log'),
            'when': 'W0',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        '': {
            'handlers': ['common_error', 'common_warning', 'common_info', 'common_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream'],
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda x: x.LANGUAGE_CODE,
        'VERIFIED_EMAIL': True,
    }
}



COMPRESS_PRECOMPILERS = (
    ('text/less', os.path.abspath(os.path.join(BASE_DIR, '..',  'lessc {infile} {outfile}'))),
)


try:    
    from core.local_settings import *
except ImportError:
    pass
 
LANGUAGES = (
    ('ru', _('Russian')),
    ('be', _('Belarusian')),
)

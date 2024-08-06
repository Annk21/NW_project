"""
Django settings for news_portal project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-lx0!6u3-zds_jkms2jfli7e7787)z7$9k$9uui7hhl&8dr!^!e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False


ALLOWED_HOSTS = ['127.0.0.1']

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'blog.apps.BlogConfig',
    'django_filters',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
    'django_apscheduler',
]

DEFAULT_FROM_EMAIL = 'alina.neus@yandex.ru'

SITE_ID = 2

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'news_portal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'news_portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [
    BASE_DIR / "static"
]

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/news'
ACCOUNT_LOGOUT_REDIRECT_URL = '/accounts/login/'

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_FORMS = {'signup': 'blog.forms.CommonSignupForm'}

EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_POST = 465
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


ADMINS = [
    ('Alina', 'alina.neus@yandex.ru'),
]

SERVER_EMAIL = 'alina.neus@yandex.ru'

APSCHEDULER_DATETIME_FORMAT = "N j, Y, f:s a"
APSCHEDULER_RUN_NOW_TIMEOUT = 25

SITE_URL = 'http://127.0.0.1:8000'

CELERY_BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
    }
}


def debug_info_filter(message):
    return message.levelname == 'DEBUG' or message.levelname == 'INFO'


def warning_filter(message):
    return message.levelname == 'WARNING'


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'console_debug_info': {
            'format': '{asctime} {levelname} {message}',
            'style': '{',
        },
        'console_warning': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
        'console_error_critical': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'file_general_log': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'file_errors_log': {
            'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
            'style': '{',
        },
        'file_security_log': {
            'format': '{asctime} {levelname} {module} {message}',
            'style': '{',
        },
        'mail_errors_log': {
            'format': '{asctime} {levelname} {message} {pathname}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'debug_info_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': debug_info_filter,
        },
        'warning_filter': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': warning_filter,
        },
    },
    'handlers': {
        'console_debug_info': {
            'level': 'DEBUG',
            'filters': ['require_debug_true', 'debug_info_filter'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_debug_info'
        },
        'console_warning': {
            'level': 'WARNING',
            'filters': ['require_debug_true', 'warning_filter'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_warning'
        },
        'console_error_critical': {
            'level': 'ERROR',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'console_error_critical'
        },
        'file_general_log': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.FileHandler',
            'filename': 'Logging/general.log',
            'formatter': 'file_general_log'
        },
        'file_errors_log': {
            'class': 'logging.FileHandler',
            'filename': 'Logging/errors.log',
            'formatter': 'file_errors_log'
        },
        'file_security_log': {
            'class': 'logging.FileHandler',
            'filename': 'Logging/security.log',
            'formatter': 'file_security_log'
        },
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'mail_errors_log'
        }
    },
    'loggers': {
        'django': {
            'level': 'DEBUG',
            'handlers': ['console_debug_info', 'console_warning', 'console_error_critical', 'file_general_log'],
            'propagate': True
        },
        'django.request': {
            'level': 'ERROR',
            'handlers': ['file_errors_log', 'mail_admins'],
        },
        'django.server': {
            'level': 'ERROR',
            'handlers': ['file_errors_log', 'mail_admins'],
        },
        'django.template': {
            'level': 'ERROR',
            'handlers': ['file_errors_log'],
        },
        'django.db_backends': {
            'level': 'ERROR',
            'handlers': ['file_errors_log'],
        },
        'django.security': {
            'level': 'DEBUG',
            'handlers': ['file_security_log'],
        },
    }
}
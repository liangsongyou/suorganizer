"""
Django settings for suorganizer project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'a1xhoq3ww@e41g9_c$vu81-t+4)i+%*r71j@ck!d8#_qt3$^#@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

SITE_ID = 1


# Application definition

INSTALLED_APPS = (
    'user',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django_extensions',
    'organizer',
    'blog',
    'contact',
    'core',
    'django.contrib.admin',

)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

ROOT_URLCONF = 'suorganizer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
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

WSGI_APPLICATION = 'suorganizer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)


# Email

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
SERVER_EMAIL = 'contact@django-unleashed.com'
DEFAULT_FROM_EMAIL = 'no-reply@django-unleashed.com'
EMAIL_SUBJECT_PREFIX = '[Startup Organizer]'
MANAGERS = (
    ('Us', 'ourselves@django-unleashed.com'),
)

# Loging

from .log_filters import ManagementFilter

verbose = (
        "[%(asctime)s] %(levelname)s"
        "[%(name)s:%(lineno)s] %(message)s")

LOGGING = {
    'version': 1,
    'disable_existing_loggers':False,
    'filters':{
        'remove_migration_sql':{
            '()': ManagementFilter,
        },
    },
    'handlers':{
        'console':{
            'class':'logging.StreamHandler'
        },
    },
    'formatters':{
        'verbose':{
            'format': verbose,
            'datefmt':"%Y-%b-%c %H:%M:%S"
        },
    },
    'loggers':{
        'django':{
            'handlers':['console'],
            'level':'DEBUG',
            'formatter':'verbose'
        }

    },


}


# Login

from django.core.urlresolvers import reverse_lazy

LOGIN_REDIRECT_URL = reverse_lazy('blog_post_list')
LOGIN_URL = reverse_lazy('dj-auth:login')
LOGOUT_URL = reverse_lazy('dj-auth:logout')


# User

AUTH_USER_MODEL = 'user.User'

# Fixture

FIXTURE_DIRS = (os.path.join(BASE_DIR,'fixtures'),)





















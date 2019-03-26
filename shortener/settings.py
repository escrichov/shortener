"""
Django settings for shortener project.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""
import os
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from django.utils.translation import ugettext_lazy as _


def envbool(s, default):
    v = os.getenv(s, default=default)
    if v not in ("", "True", "False"):
        msg = "Unexpected value %s=%s, use 'True' or 'False'" % (s, v)
        raise Exception(msg)
    return v == "True"


def envint(s, default):
    v = os.getenv(s, default)
    if v == "None":
        return None

    return int(v)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = envbool("DJANGO_DEBUG", "False")

ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "*").split(",")

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    'django_extensions',
    'payments',
    'shortener_app',
    'users',
    'django.contrib.admin',
    'rest_framework',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'shortener.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'shortener.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.getenv("DB_NAME", os.path.join(BASE_DIR, 'db.sqlite3')),
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME':
        'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME':
        'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/
LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LANGUAGES = (
    ('en', _('English')),
    ('es', _('Spanish')),
)

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

AUTH_USER_MODEL = 'users.User'

LOGIN_REDIRECT_URL = 'shortener_app:urls'
LOGOUT_REDIRECT_URL = 'shortener_app:index'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',),
    'DEFAULT_PARSER_CLASSES': ('rest_framework.parsers.JSONParser',),
    'DEFAULT_AUTHENTICATION_CLASSES':
    ('shortener_app.authentication.APIAccessAuthentication',),
    'DEFAULT_PERMISSION_CLASSES':
    ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_PAGINATION_CLASS':
    'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE':
    10
}

DEFAULT_FROM_EMAIL = 'Cour.fun <info@cour.fun>'
EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = os.path.join(BASE_DIR, "sent_emails")

IPSTACK_APIKEY = os.getenv("DJANGO_IPSTACK_APIKEY")

STRIPE_PUBLIC_KEY = os.getenv("DJANGO_STRIPE_PUBLIC_KEY")
STRIPE_SECRET_KEY = os.getenv("DJANGO_STRIPE_SECRET_KEY")

SEGMENT_ANALYTICS_WRITE_KEY = os.getenv("DJANGO_SEGMENT_ANALYTICS_WRITE_KEY")
SEGMENT_ANALYTICS_DEBUG = envbool("SEGMENT_ANALYTICS_DEBUG", 'True')

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    },
}
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 100
CACHE_MIDDLEWARE_KEY_PREFIX = ''
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

USE_S3 = envbool("DJANGO_USE_S3", False)
if USE_S3:
    AWS_DEFAULT_ACL = None
    AWS_ACCESS_KEY_ID = os.getenv("DJANGO_AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("DJANGO_AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = os.getenv("DJANGO_AWS_STORAGE_BUCKET_NAME")
    AWS_LOCATION = 'static'
    AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': 'max-age=86400',
    }

    STATIC_URL = 'https://%s/%s/' % (AWS_S3_CUSTOM_DOMAIN, AWS_LOCATION)

    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
else:
    STATIC_URL = '/static/'

# Security
SESSION_COOKIE_SECURE = envbool("DJANGO_SESSION_COOKIE_SECURE", "True")
SECURE_BROWSER_XSS_FILTER = envbool("DJANGO_SECURE_BROWSER_XSS_FILTER", "True")
SECURE_CONTENT_TYPE_NOSNIFF = envbool("DJANGO_SECURE_CONTENT_TYPE_NOSNIFF", "True")
SECURE_HSTS_INCLUDE_SUBDOMAINS = envbool("DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS", "True")
SECURE_HSTS_SECONDS = envint("DJANGO_SECURE_HSTS_SECONDS", "31536000")
SECURE_REDIRECT_EXEMPT = os.getenv("DJANGO_SECURE_REDIRECT_EXEMPT", [])
SECURE_SSL_HOST = os.getenv("DJANGO_SECURE_SSL_HOST_SECURE_SSL_HOST")
SECURE_SSL_REDIRECT = envbool("DJANGO_SECURE_SSL_REDIRECT", "False")
#SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

HOSTNAME = 'https://cour.fun'

EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
SENDGRID_API_KEY = os.getenv('DJANGO_SENDGRID_API_KEY')

SENTRY_DSN = os.getenv('DJANGO_SENTRY_DSN')

if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[DjangoIntegration()])


CACHES = {
    'default': {
        'BACKEND': 'redis_cache.RedisCache',
        'LOCATION': os.getenv('REDIS_URL'),
    },
}

if os.path.exists(os.path.join(BASE_DIR, "shortener/local_settings.py")):
    from .local_settings import *
else:
    warnings.warn("local_settings.py not found, using defaults")

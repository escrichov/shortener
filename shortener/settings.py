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
from configurations import Configuration, values


class Common(Configuration):
    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])

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
    ]

    MIDDLEWARE = [
        'django.middleware.cache.UpdateCacheMiddleware', # This must be first on the list
        'django.middleware.security.SecurityMiddleware',
        'whitenoise.middleware.WhiteNoiseMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.locale.LocaleMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'django.middleware.cache.FetchFromCacheMiddleware', # This must be last
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
    DATABASES = values.DatabaseURLValue('sqlite:///{}'.format(
        os.path.join(BASE_DIR, 'db.sqlite3')))

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
    STATIC_URL = '/static/'
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

    IPSTACK_APIKEY = values.SecretValue()

    STRIPE_PUBLIC_KEY = values.SecretValue()
    STRIPE_SECRET_KEY = values.SecretValue()

    SEGMENT_ANALYTICS_WRITE_KEY = values.SecretValue()
    SEGMENT_ANALYTICS_DEBUG = values.BooleanValue(True)

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        },
    }
    CACHE_MIDDLEWARE_ALIAS = 'default'
    CACHE_MIDDLEWARE_SECONDS = 100
    CACHE_MIDDLEWARE_KEY_PREFIX = ''
    SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = True

    INTERNAL_IPS = ['127.0.0.1']

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]
    import django.contrib.auth.hashers
    PASSWORD_HASHERS = [
        'django.contrib.auth.hashers.MD5PasswordHasher',
    ]

    HOSTNAME = 'http://localhost:8000'

    #EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    #SENDGRID_API_KEY = values.SecretValue()
    #SENDGRID_SANDBOX_MODE_IN_DEBUG = True


class Staging(Common):
    """
    The in-staging settings.
    """
    ALLOWED_HOSTS = ['carlos-shortener.herokuapp.com', 'cour.fun']

    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(False)
    #SECURE_PROXY_SSL_HEADER = values.TupleValue(
    #    ('HTTP_X_FORWARDED_PROTO', 'https')
    #)

    HOSTNAME = 'https://cour.fun'

    EMAIL_BACKEND = "sendgrid_backend.SendgridBackend"
    SENDGRID_API_KEY = values.SecretValue()

    SENTRY_DSN = values.SecretValue()

    REDIS_URL = values.SecretValue(
        environ_name='REDIS_URL', environ_prefix=None)
    CACHES = {
        'default': {
            'BACKEND': 'redis_cache.RedisCache',
            'LOCATION': REDIS_URL,
        },
    }

    @classmethod
    def post_setup(cls):
        sentry_sdk.init(dsn=cls.SENTRY_DSN, integrations=[DjangoIntegration()])


class Production(Staging):
    """
    The in-production settings.
    """
    pass

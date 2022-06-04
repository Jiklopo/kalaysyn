import dj_database_url
from configuration.sentry import init_sentry

from os import getenv
from pathlib import Path
from datetime import timedelta

init_sentry()
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = getenv('SECRET_KEY', '123456')
DEBUG = bool(getenv('DEBUG'))

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    getenv('APP_URL', '0.0.0.0')
]

CSRF_TRUSTED_ORIGINS = [
    getenv('TRUSTED_ORIGIN', 'http://localhost')
]

LOCAL_APPS = [
    'apps.authentication',
    'apps.records',
    'apps.health',
    'apps.qr',
    'apps.profile',
    'apps.goals',
    'apps.psytests',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'drf_spectacular',
    'rest_framework_simplejwt',
    'storages',
]

INSTALLED_APPS = [
    'jazzmin',  # This app must be before django.contrib.admin

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    *THIRD_PARTY_APPS,
    *LOCAL_APPS,
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'apps.common.middleware.JsonExceptionMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'rest_framework.views.exception_handler',
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Kalaysyn API',
    'DESCRIPTION': 'API for Kalaysyn mobile app',
    'VERSION': '0.0.1',
    'SERVE_INCLUDE_SCHEMA': False
}

ROOT_URLCONF = 'configuration.urls'
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

WSGI_APPLICATION = 'configuration.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default='postgres://postgres:password@db:5432/postgres', conn_max_age=600)
}

# Authentication
AUTH_USER_MODEL = 'authentication.User'

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

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=365),
}

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Celery
CELERY_BROKER_URL = getenv('REDIS_URL', 'redis://redis:6379')
CELERY_RESULT_BACKEND = getenv('REDIS_URL', 'redis://redis:6379')
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TASK_SERIALIZER = 'json'

# Files configuration
STATIC_URL = f'{getenv("AWS_LOCATION")}/static/'
STATIC_ROOT = STATIC_ROOT = BASE_DIR / "staticfiles-cdn"
STATICFILES_STORAGE = 'configuration.cdn.StaticRootS3BotoStorage'
DEFAULT_FILE_STORAGE = 'configuration.cdn.MediaRootS3BotoStorage'

# AWS
AWS_S3_ACCESS_KEY_ID=getenv('AWS_S3_ACCESS_KEY_ID')
AWS_S3_SECRET_ACCESS_KEY=getenv('AWS_S3_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_ENDPOINT_URL = getenv('AWS_S3_ENDPOINT_URL')
AWS_LOCATION = getenv('AWS_LOCATION')
AWS_S3_OBJECT_PARAMETERS = {
    "CacheControl": "max-age=86400",
    "ACL": "public-read"
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST = getenv('EMAIL_HOST')
EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# App settings
CODE_VALID_SECONDS = 300

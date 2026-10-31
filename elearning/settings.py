


from pathlib import Path
import os
from dotenv import load_dotenv

from django.core.files import locks
import pymysql


pymysql.install_as_MySQLdb()



load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-n!a*dy+qce9)1@$1-r^^7mm*0!^a_9mat_%ujfvj@+@ng@14cs'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'storages',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # Redis session support here
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'elearning.middleware.TrackVisitMiddleware',
]

ROOT_URLCONF = 'elearning.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'main' / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'elearning.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'

# AWS S3 Media files (as before)
MEDIA_URL = f'https://{os.getenv("AWS_S3_CUSTOM_DOMAIN", "ppl-ai-file-upload.s3.amazonaws.com")}/'

AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


SESSION_CACHE_ALIAS = "default"

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EcoCash API credentials
ECOCASH_CLIENT_ID = os.getenv('ECOCASH_CLIENT_ID', "your_ecocash_client_id_here")
ECOCASH_CLIENT_SECRET = os.getenv('ECOCASH_CLIENT_SECRET', "your_ecocash_client_secret_here")

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/results/'



WOLFRAMALPHA_APP_ID = os.getenv('WOLFRAMALPHA_APP_ID')
locks.lock = lambda f, flags: None
locks.unlock = lambda f: None




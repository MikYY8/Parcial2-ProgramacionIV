from pathlib import Path
from dotenv import load_dotenv
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&vf0b3n-uhq$g96bj%nc@zzlk^_9yj+lc($&2hj&4gkcrf$^m='


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

load_dotenv()

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"  # esta palabra literal
EMAIL_HOST_PASSWORD = "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"
DEFAULT_FROM_EMAIL = "mica.yaz03@gmail.com"

LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "login"


ALLOWED_HOSTS = ["*"]

# Application definition

BASE = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

TERCEROS = [
    'rest_framework',
    'widget_tweaks',
    'drf_yasg',
    'reportlab',
]

PROPIAS = [
    'users',
    'alumnos',
    'scraper',
]

INSTALLED_APPS = BASE + TERCEROS + PROPIAS

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend',
)

AUTH_USER_MODEL = 'users.User'


LOGIN_URL = '/login/'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Parcial.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Parcial.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]


# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

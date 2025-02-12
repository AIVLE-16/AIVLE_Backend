"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 5.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
import json
from django.core.exceptions import ImproperlyConfigured



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-7&xn=^%mc@2gxlw(z=a-ybgb0nslzs%l7l34!p5!!cz@c*x38*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "stt",
    "channels", # ASGI 설정
    'rest_framework',
    'corsheaders', # CORS 헤더 설정
    'account',     # 회원 설정
    'api',         # 모델 api
    'post',        # 게시판 app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware', # CORS 헤더 설정
    
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "DB.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ASGI_APPLICATION = 'config.asgi.application' # ASGI 설정

CORS_ORIGIN_ALLOW_ALL = True # CORS 헤더 설정

# # 보안을 위해 외부에 저장된 secret.json 불러오기
# with open("config/secret.json") as f:
#     secrets = json.loads(f.read())

# # Secret 설정값 가져오기
# def get_secret(setting, secrets=secrets):
#     try:
#         return secrets[setting]
#     except KeyError:
#         error_msg = f"Set the {setting} enviroment variable"
#         raise ImproperlyConfigured(error_msg)

# # SECRET_KEY 값
# SECRET_KEY = get_secret("SECRET_KEY")

# SMTP 세팅 추가
from . import smtp_settings

DATABASES  = smtp_settings.DATABASES
SECRET_KEY = smtp_settings.SECRET_KEY

EMAIL_BACKEND       = smtp_settings.EMAIL['EMAIL_BACKEND']
EMAIL_USE_TLS       = smtp_settings.EMAIL['EMAIL_USE_TLS']      
EMAIL_PORT          = smtp_settings.EMAIL['EMAIL_PORT']                
EMAIL_HOST          = smtp_settings.EMAIL['EMAIL_HOST']
EMAIL_HOST_USER     = smtp_settings.EMAIL['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = smtp_settings.EMAIL['EMAIL_HOST_PASSWORD']
DEFAULT_FROM_EMAIL  = smtp_settings.EMAIL['DEFAULT_FROM_EMAIL']
SERVER_EMAIL        = smtp_settings.EMAIL['SERVER_EMAIL']

# 서버 캐시 설정
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# CORS 설정
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
]

# 파일 저장 위치
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
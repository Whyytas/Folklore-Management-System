"""
Django settings for FolkloreManagementSystem project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

import os

# ✅ Define the static URL
STATIC_URL = '/static/'

# ✅ Define where static files are collected
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# ✅ Define where Django looks for static files inside the project
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Ensure this directory exists
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-+_n6j3p7xr&pcxd1ujofrbs!k6hm^=ijg*6t#qgd5dm$_9*j50'
YOUTUBE_API_KEY = "AIzaSyAX8QZHAYYSdEozYqHwH2XytcmrOG055Bo"


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['folklore.azurewebsites.net',
                 'localhost',
                 '127.0.0.1']

LOGIN_URL='/'

LOGIN_REDIRECT_URL = '/main'
LOGOUT_REDIRECT_URL = '/'  # Redirect to homepage after logout

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = ['https://folklore.azurewebsites.net']
OAUTH2_PROVIDER = {
    'ACCESS_TOKEN_EXPIRE_SECONDS': 3600,
    'APPLICATION_MODEL': 'oauth2_provider.Application',
    'SCOPES': {'read': 'Read scope', 'write': 'Write scope'},
    'OAUTH2_VALIDATOR_CLASS': 'Initial.validators.CustomOAuth2Validator',  # Correct path to validator
}
AUTH_USER_MODEL = 'Initial.User'

REST_FRAMEWORK = {

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',  # Require authentication
    ),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'MyFolkloreApis',
    'DESCRIPTION': 'Lorem ipsum dolor sit amet',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    # OTHER SETTINGS
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.py.IsAuthenticated',
    ),
}
# Application definition

INSTALLED_APPS = [
    'Initial',  # Place your user model app first
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'oauth2_provider',
    'Padaliniai',
    'Programos',
    'Kuriniai',
    'Renginiai',
    'Ansambliai',
    'Instrumentai',
    'Nariai',
    'Repeticijos'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'FolkloreManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"]
        ,
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

WSGI_APPLICATION = 'FolkloreManagementSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'allData',
        'USER': 'adminas',
        'PASSWORD': 'Bebaimis100.',
        'HOST': 'folkloredata.postgres.database.azure.com',
        'PORT': '5432',
        'OPTIONS': {'sslmode': 'require'},

    }
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

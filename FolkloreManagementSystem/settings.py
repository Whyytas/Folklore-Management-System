"""
Django settings for FolkloreManagementSystem project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information, see:
- https://docs.djangoproject.com/en/5.1/topics/settings/
- https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from .env in local development
if os.getenv("ENV") != "PRODUCTION":
    load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Time zone and language settings
TIME_ZONE = "Europe/Vilnius"
USE_TZ = False
LANGUAGE_CODE = "lt"  # Lithuanian
DATE_FORMAT = "Y-m-d"  # YYYY-MM-DD
DATETIME_FORMAT = "Y-m-d H:i"

# Security keys (ensure these are stored securely)
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
RESEND_API_KEY = os.getenv("RESEND_API_KEY")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL")

if not SECRET_KEY:
    raise ValueError("Missing DJANGO_SECRET_KEY environment variable")

# Debug mode (should be False in production)
DEBUG = True

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
# Allowed hosts
ALLOWED_HOSTS = [
    "folklore.azurewebsites.net",
    "localhost",
    "127.0.0.1",
]

# Azure Storage Settings
AZURE_ACCOUNT_NAME = "instrumentstorage"
AZURE_ACCOUNT_KEY = os.getenv("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = "instrument-photos"
AZURE_CUSTOM_DOMAIN = f"{AZURE_ACCOUNT_NAME}.blob.core.windows.net"

if not AZURE_ACCOUNT_KEY:
    raise ValueError("Missing AZURE_ACCOUNT_KEY environment variable")

# Media storage using Azure Blob Storage
DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
MEDIA_URL = f"https://{AZURE_CUSTOM_DOMAIN}/{AZURE_CONTAINER}/"

# Static file settings
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Authentication and authorization settings
LOGIN_URL = "/"
LOGIN_REDIRECT_URL = "/main"
LOGOUT_REDIRECT_URL = "/"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "file": {
            "level": "ERROR",
            "class": "logging.FileHandler",
            "filename": os.path.join(BASE_DIR, "django-errors.log"),
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = ["https://folklore.azurewebsites.net"]

# OAuth2 settings
OAUTH2_PROVIDER = {
    "ACCESS_TOKEN_EXPIRE_SECONDS": 3600,
    "APPLICATION_MODEL": "oauth2_provider.Application",
    "SCOPES": {"read": "Read scope", "write": "Write scope"},
    "OAUTH2_VALIDATOR_CLASS": "Initial.validators.CustomOAuth2Validator",
}

AUTH_USER_MODEL = "Initial.User"

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": ("oauth2_provider.contrib.rest_framework.OAuth2Authentication",),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# DRF Spectacular settings (OpenAPI schema)
SPECTACULAR_SETTINGS = {
    "TITLE": "MyFolkloreApis",
    "DESCRIPTION": "Lorem ipsum dolor sit amet",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
}

# Installed apps
INSTALLED_APPS = [
    "Initial",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "oauth2_provider",
    "Padaliniai",
    "Programos",
    "Kuriniai",
    "Renginiai",
    "Ansambliai",
    "Instrumentai",
    "Nariai",
    "Repeticijos",
    "Kalendorius",
    "mainPage",
    "debug_toolbar",
]

# Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
"debug_toolbar.middleware.DebugToolbarMiddleware",

    # Catch unhandled errors
    "FolkloreManagementSystem.middlewares.CatchAllExceptionsMiddleware",
]

# URL configuration
ROOT_URLCONF = "FolkloreManagementSystem.urls"

# Templates configuration
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

# WSGI application
WSGI_APPLICATION = "FolkloreManagementSystem.wsgi.application"

# Database configuration (Use environment variables for security)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME"),
        "USER": os.getenv("DB_USER"),
        "PASSWORD": os.getenv("DB_PASSWORD"),
        "HOST": os.getenv("DB_HOST"),
        "PORT": os.getenv("DB_PORT"),
        "OPTIONS": {"sslmode": "require"},
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

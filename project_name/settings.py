"""
Django settings for {{ project_name }} project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
import os
import re
from pathlib import Path

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "override me")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv("NODEBUG") is None else False

# TODO: Change your domain names here.
ALLOWED_HOSTS = ["*"] if os.getenv("NODEBUG") is None else [".yourdomain.com"]

# TODO: Change the default "from" email here.
DEFAULT_FROM_EMAIL = "me@mydomain.com"

# TODO: Add environment variables for this, "production", "staging".
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")

# Sometimes my CSRF protection would fail locally due to misdetection of HTTPS as HTTPS.
# If you don't need this, you can remove it, but it shouldn't hurt anything.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sites",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "django_extensions",
    "djangoql",
    "main",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "{{ project_name }}.middleware.StatsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.sites.middleware.CurrentSiteMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "{{ project_name }}.urls"

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
                "{{ project_name }}.context_processors.settings",
            ]
        },
    }
]

TEMPLATE_STRING_IF_INVALID = "VARIABLE UNDEFINED: %s"

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"

WSGI_APPLICATION = "{{ project_name }}.wsgi.application"

AUTH_USER_MODEL = "main.User"

# Adjust this to taste.
SESSION_ENGINE = "django.contrib.sessions.backends.cached_db"

if os.getenv("IN_DOCKER"):
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "password",
            "HOST": "db",
            "PORT": 5432,
            # Keep connections in the pool for an hour.
            "CONN_MAX_AGE": 60 * 60,
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": "redis://redis/1",
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

    SESSION_CACHE_ALIAS = "default"
    SESSION_COOKIE_AGE = 365 * 24 * 60 * 60
elif os.getenv("DATABASE_URL"):
    # Running under Dokku.
    USER, PASSWORD, HOST, PORT, NAME = re.match(  # type: ignore
        r"^postgres://(?P<username>.*?)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/(?P<db>.*?)$",
        os.getenv("DATABASE_URL", ""),
    ).groups()

    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql_psycopg2",
            "NAME": NAME,
            "USER": USER,
            "PASSWORD": PASSWORD,
            "HOST": HOST,
            "PORT": int(PORT),
            # Keep connections in the pool for an hour.
            "CONN_MAX_AGE": 60 * 60,
        }
    }

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.getenv("REDIS_URL", ""),
            "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
        }
    }

    SESSION_CACHE_ALIAS = "default"
    SESSION_ENGINE = "django.contrib.sessions.backends.cache"
    SESSION_COOKIE_AGE = 365 * 24 * 60 * 60
    SESSION_COOKIE_SECURE = True
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

if os.getenv("EMAIL_URL", ""):
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_HOST, EMAIL_PORT = re.match(  # type: ignore
        r"^email://(?P<username>.*)\:(?P<password>.*?)\@(?P<host>.*?)\:(?P<port>\d+)\/?$",
        os.getenv("EMAIL_URL", ""),
    ).groups()
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SITE_ID = 1

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=0.2,
    environment=ENVIRONMENT,
    integrations=[DjangoIntegration()],
)

TEST_RUNNER = "xmlrunner.extra.djangotestrunner.XMLTestRunner"

TEST_OUTPUT_FILE_NAME = "report.xml"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": os.getenv("DJANGO_LOG_LEVEL", "INFO"),
        }
    },
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "_static"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STATICFILES_DIRS = [BASE_DIR / "static"]

from dotenv import load_dotenv
from pathlib import Path
import base64
import sys
import os

env_file_path: str = os.getcwd() + "/.env"

env_loaded: bool = load_dotenv(dotenv_path=env_file_path, override=True)
DB_NAME: str = os.getenv("DB_NAME", "")
DB_USER: str = os.getenv("DB_USER", "")
DB_PASS:str = os.getenv("DB_PASS", "")
DB_HOST: str = os.getenv("DB_HOST", "")

APP_NAME: str = os.getenv("APP_NAME", "django base app")
APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "django base app")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent


DEFAULT_SECRET_KEY: str = 'django-insecure-dca8=1qpcbj*8!97yxaihy8!(0#*f)uosxqrsh&3oy)44&s$m6'
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)

ENV_NAME: str = os.getenv("ENV_NAME", "DEV")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = ENV_NAME == "DEV"

if SECRET_KEY == DEFAULT_SECRET_KEY and ENV_NAME != "DEV":
    raise Exception("Can't use default env secret key for production")

ALLOWED_HOSTS: list[str] = os.getenv("ALLOWED_HOSTS", "").split(",") if not DEBUG else ["*"]


# Application definition


DJANGO_APPS: list[str] = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "django_filters",
]

USER_APPS: list[str] =[
    'apps.apps.AppsConfig',
    'api.apps.ApiConfig',
]

THIRD_PARTY: list[str] = [
    'jazzmin',
    "rest_framework",
    "rest_framework.authtoken",
    "drf_yasg",
]

INSTALLED_APPS: list[str] = THIRD_PARTY + DJANGO_APPS + USER_APPS

REST_FRAMEWORK: dict[str, list|int|str] = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly",
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

MIDDLEWARE: list[str] = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
]

# DJANGO_APPS = DJANGO_APPS + MIDDLEWARE

ROOT_URLCONF: str = 'config.urls'

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

STORAGES = {
    # ...
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES: dict[str, dict[str, str]] = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
        "HOST": DB_HOST,
        "PORT": "5432",
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_database",
        "OPTIONS": {
            "timeout": 20,
        }
    }

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Token': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header',
            'description': 'Token-based authentication using the format: Token <your-token>',
        }
    }
}
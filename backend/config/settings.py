from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv
from datetime import timedelta
from pathlib import Path
import sys
import os

env_file_path: str = os.getcwd() + "/.env"

env_loaded: bool = load_dotenv(dotenv_path=env_file_path, override=True)


def env_bool(name: str, default: bool = False) -> bool:
    value = os.getenv(name)
    if value is None or value == "":
        return default
    return value.lower() in ("true", "1", "yes")


def env_list(name: str, default: str = "") -> list[str]:
    return [item.strip() for item in os.getenv(name, default).split(",") if item.strip()]


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Database
# DB_ENGINE: sqlite (default), postgresql or mysql
DB_ENGINE: str = os.getenv("DB_ENGINE", "").lower() or "sqlite"
DB_NAME: str = os.getenv("DB_NAME", "")
DB_USER: str = os.getenv("DB_USER", "")
DB_PASS: str = os.getenv("DB_PASS", "")
DB_HOST: str = os.getenv("DB_HOST", "")
DB_PORT: str = os.getenv("DB_PORT", "")

USE_REDIS_CACHE: bool = env_bool("USE_REDIS_CACHE")
if USE_REDIS_CACHE:
    REDIS_HOST: str = os.getenv("REDIS_HOST", "127.0.0.1")
    REDIS_DB_INDEX: int = int(os.getenv("REDIS_DB_INDEX", "1"))
    REDIS_USE_SSL: bool = env_bool("REDIS_USE_SSL")
    REDIS_PORT: int = int(os.getenv("REDIS_PORT", "6380" if REDIS_USE_SSL else "6379"))
    REDIS_VALIDATE_CERT: bool = env_bool("REDIS_VALIDATE_CERT")
    REDIS_SSL_CA_CERTS: str | None = os.getenv("REDIS_SSL_CA_CERTS")
    REDIS_PASSWORD: str = os.getenv("REDIS_PASSWORD", "")

    def redis_url(db_index: int) -> str:
        return "{connection_type}://{auth}{host}:{port}/{db_index}".format(
            connection_type="rediss" if REDIS_USE_SSL else "redis",
            auth=f":{REDIS_PASSWORD}@" if REDIS_PASSWORD else "",
            host=REDIS_HOST,
            port=REDIS_PORT,
            db_index=db_index,
        )

    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": redis_url(REDIS_DB_INDEX),
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
        }
    }

APP_NAME: str = os.getenv("APP_NAME", "django base app")
APP_DESCRIPTION: str = os.getenv("APP_DESCRIPTION", "django base app")

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "info")
# Persist every Logger call into the AppLog table
LOG_TO_DB: bool = env_bool("LOG_TO_DB")
# Log every API request (method, path, status, user, ip, duration) through the Logger
LOG_REQUESTS: bool = env_bool("LOG_REQUESTS")


DEFAULT_SECRET_KEY: str = (
    "django-insecure-dca8=1qpcbj*8!97yxaihy8!(0#*f)uosxqrsh&3oy)44&s$m6"
)
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = os.getenv("SECRET_KEY", DEFAULT_SECRET_KEY)

ENV_NAME: str = os.getenv("ENV_NAME", "DEV")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG: bool = ENV_NAME == "DEV"

if SECRET_KEY == DEFAULT_SECRET_KEY and ENV_NAME != "DEV":
    raise Exception("Can't use default env secret key for production")

ALLOWED_HOSTS: list[str] = env_list("ALLOWED_HOSTS") if not DEBUG else ["*"]


# Application definition


DJANGO_APPS: list[str] = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_filters",
]

USER_APPS: list[str] = [
    "apps.apps.AppsConfig",
    "api.apps.ApiConfig",
    "apps.users.apps.UsersConfig",
    "apps.logs.apps.LogsConfig",
]

THIRD_PARTY: list[str] = [
    "jazzmin",
    "rest_framework",
    "rest_framework_simplejwt",
    "drf_spectacular",
    "corsheaders",
    "django_celery_results",
    "django_celery_beat",
]

INSTALLED_APPS: list[str] = THIRD_PARTY + DJANGO_APPS + USER_APPS

# Custom User Model (email login)
AUTH_USER_MODEL = "users.User"

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "ROTATE_REFRESH_TOKENS": True,
}

REST_FRAMEWORK: dict[str, list | int | str] = {
    # Routes under api/public/ are open, everything else requires authentication.
    # See api/permissions.py and api/authentication.py
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "api.authentication.RouteAwareJWTAuthentication"
    ],
    "DEFAULT_PERMISSION_CLASSES": ["api.permissions.IsPublicRouteOrAuthenticated"],
    "DEFAULT_FILTER_BACKENDS": ["django_filters.rest_framework.DjangoFilterBackend"],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

MIDDLEWARE: list[str] = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

if LOG_REQUESTS:
    MIDDLEWARE.append("apps.logs.middleware.RequestLogMiddleware")

ROOT_URLCONF: str = "config.urls"

CORS_ALLOW_ALL_ORIGINS = ENV_NAME == "DEV"

CORS_ALLOW_CREDENTIALS = ENV_NAME == "DEV"

CORS_ALLOWED_ORIGINS: list[str] = env_list("CORS_ALLOWED_ORIGINS")

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DB_ENGINES: dict[str, str] = {
    "sqlite": "django.db.backends.sqlite3",
    "postgresql": "django.db.backends.postgresql",
    "mysql": "django.db.backends.mysql",
}
DB_DEFAULT_PORTS: dict[str, str] = {"postgresql": "5432", "mysql": "3306"}

if DB_ENGINE not in DB_ENGINES:
    raise ImproperlyConfigured(
        f"Invalid DB_ENGINE '{DB_ENGINE}'. Options: {', '.join(DB_ENGINES)}"
    )

if DB_ENGINE == "sqlite":
    DATABASES: dict[str, dict] = {
        "default": {
            "ENGINE": DB_ENGINES["sqlite"],
            "NAME": DB_NAME or BASE_DIR / "db.sqlite3",
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": DB_ENGINES[DB_ENGINE],
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASS,
            "HOST": DB_HOST,
            "PORT": DB_PORT or DB_DEFAULT_PORTS[DB_ENGINE],
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Single Page Application served by the backend itself.
# SPA_DIR must contain the built frontend (index.html + assets).
# Files are served from the root (/assets/..., /favicon.ico) by WhiteNoise and any
# route outside api/, admin/ and static/ falls back to index.html (client-side routing).
SERVE_SPA: bool = env_bool("SERVE_SPA")
SPA_DIR: Path = Path(os.getenv("SPA_DIR", "") or BASE_DIR / "spa")
if SERVE_SPA:
    WHITENOISE_ROOT = SPA_DIR

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

if "test" in sys.argv:
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "test_database",
        "OPTIONS": {
            "timeout": 20,
        },
    }

# OpenAPI 3 schema (drf-spectacular). JWT security scheme in api/schema.py
SPECTACULAR_SETTINGS = {
    "TITLE": APP_NAME,
    "DESCRIPTION": APP_DESCRIPTION,
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    # Schema is public and must not fail when the browser sends an expired token
    "SERVE_AUTHENTICATION": [],
    # Tags by app (users, token...) instead of public/private
    "SCHEMA_PATH_PREFIX": r"/api/(public|private)",
    # Separate request/response components so write only fields (password) are correct
    "COMPONENT_SPLIT_REQUEST": True,
    "SWAGGER_UI_SETTINGS": {
        "persistAuthorization": True,
    },
}

# Celery Configuration
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "")
if not CELERY_BROKER_URL and USE_REDIS_CACHE:
    # Build Celery broker URL from Redis settings (DB 0 for broker, REDIS_DB_INDEX for cache)
    CELERY_BROKER_URL = redis_url(0)

CELERY_RESULT_BACKEND = "django-db"  # Use Django database for task results (visible in admin)
CELERY_CACHE_BACKEND = "django-cache"  # Use Django cache for intermediate results
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE
CELERY_ENABLE_UTC = True
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_TASK_SOFT_TIME_LIMIT = 25 * 60  # 25 minutes
CELERY_WORKER_PREFETCH_MULTIPLIER = 4
CELERY_WORKER_MAX_TASKS_PER_CHILD = 1000
CELERY_RESULT_EXTENDED = True  # Store more detailed task result information
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"  # Use database for periodic tasks

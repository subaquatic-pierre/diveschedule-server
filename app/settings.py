import os
from pathlib import Path
from datetime import timedelta
from .config import Config

config = Config()

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = config.SECRET_KEY
DEBUG = config.DEBUG
APPEND_SLASH = False

# Base Settings
WSGI_APPLICATION = "app.wsgi.application"
ROOT_URLCONF = "app.urls"

# Application definition
INSTALLED_APPS = [
    # Default apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Dango allauth
    "django.contrib.sites",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # 'allauth.socialaccount.providers.facebook',
    # 'allauth.socialaccount.providers.google',
    # Other apps
    "graphene_django",
    "corsheaders",
    "django_filters",
    # User apps
    "app.schedule",
    "app.users",
    "app.graphql",
]

AUTH_USER_MODEL = "users.CustomUser"

# DJANGO-ALAUTH
ACCOUNT_EMAIL_VERIFICATION = None
SITE_ID = 1
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGIN_URL = "login/"
LOGIN_REDIRECT_URL = "/"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTHENTICATION_BACKENDS = [
    "graphql_jwt.backends.JSONWebTokenBackend",
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

GRAPHENE = {
    "SCHEMA": "app.graphql.schema.schema",
    "RELAY_CONNECTION_ENFORCE_FIRST_OR_LAST": True,
    "RELAY_CONNECTION_MAX_LIMIT": 100,
    "SCHEMA_OUTPUT": "graphql/schema.graphql",  # defaults to schema.json,
    "SCHEMA_INDENT": 2,  # Defaults to None (displays all data on a single line)
    "MIDDLEWARE": [
        "graphql_jwt.middleware.JSONWebTokenMiddleware",
    ],
}


GRAPHQL_JWT = {
    "JWT_VERIFY_EXPIRATION": False,
    "JWT_REFRESH_EXPIRATION_DELTA": timedelta(days=7),
}

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

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILES
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

STATIC_ROOT = os.path.join(BASE_DIR, "static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")

# Check produciton or development environment
if DEBUG:
    # CORS settings
    ALLOWED_HOSTS = ["*"]
    CSRF_TRUSTED_ORIGINS = ["*"]
    CORS_ALLOW_ALL_ORIGINS = True

    # Databse settings
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.DB_NAME,
            "USER": config.DB_USER,
            "PASSWORD": config.DB_PASSWORD,
            "HOST": config.DB_HOST,
            "PORT": config.DB_PORT,
        }
    }
    # DATABASES = {
    #     "default": {
    #         "ENGINE": "django.db.backends.sqlite3",
    #         "NAME": os.path.join(BASE_DIR, "db.sqlite"),
    #     }
    # }

else:
    # CORS settings
    CORS_ALLOW_ALL_ORIGINS = True
    CSRF_TRUSTED_ORIGINS = config.CSRF_TRUSTED_ORIGINS
    ALLOWED_HOSTS = config.ALLOWED_HOSTS

    # Database settings
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.DB_NAME,
            "USER": config.DB_USER,
            "PASSWORD": config.DB_PASSWORD,
            "HOST": config.DB_HOST,
            "PORT": config.DB_PORT,
        }
    }

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

# ---------------------- HIDE ALL BELOW FOR SECURITY ----------------------

# SOCIALACCOUNT_PROVIDERS = {
#     'google': {
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     },
#     'facebook': {
#         'APP': {
#             'client_id': '123',
#             'secret': '456',
#             'key': ''
#         }
#     }
# }

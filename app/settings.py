import os
from datetime import timedelta
from .config import Config

config = Config()

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))

SECRET_KEY = config.SECRET_KEY

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
    "JWT_EXPIRATION_DELTA": False,
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

APPEND_SLASH = False

# INTERNATIONALIZATION
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# STATIC FILES
MEDIA_ROOT = os.path.join(PROJECT_ROOT, "media")
MEDIA_URL = os.environ.get("MEDIA_URL", "/media/")

STATIC_ROOT = os.path.join(PROJECT_ROOT, "static")
STATIC_URL = os.environ.get("STATIC_URL", "/static/")

# Check produciton or development environment
if config.DATABASE == "AWS":
    ALLOWED_HOSTS = [".divesandybeach.com"]
    DEBUG = False
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config.NAME,
            "USER": config.USER,
            "PASSWORD": config.PASSWORD,
            "HOST": config.HOST,
            "PORT": config.PORT,
        }
    }

    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
        },
        {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
        {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
        {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
    ]

# development environment
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
    DEBUG = True
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(PROJECT_ROOT, "db.sqlite"),
        }
    }

    # Cors Header Settings
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_ALLOW_ALL = True
    CSRF_COOKIE_NAME = "csrftoken"

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

# TODO:
# Setup email backend for forgotten password
# Add react-helmet to front end
# Use django-all-auth

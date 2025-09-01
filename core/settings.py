from datetime import timedelta
import os
from pathlib import Path
from decouple import config, Csv

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", default=False, cast=bool)

TG_ADMINS = config("ADMINS", cast=Csv())
ADMIN = config("ADMIN")
ALLOWED_HOSTS = config("ALLOWED_HOSTS", cast=Csv())
TELEGRAM_BOT_TOKEN = config("BOT_TOKEN")
GROUP_ID = config("GROUP_ID", default="6357730441")

# Application definition
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # THIRD PARTY APPS
    "rest_framework",
    "rest_framework_simplejwt",  # Add this for JWT
    "rest_framework_simplejwt.token_blacklist",
    "phonenumber_field",
    "drf_yasg",
    "django_filters",
    "corsheaders",  # Add this for CORS handling
    # LOCAL APPS
    "account",
    "user",
    "advance",
    "exchange.apps.ExchangeConfig",
    "local_trading.apps.LocalTradingConfig",
    "bot.apps.BotConfig",
]

# Custom User Model
AUTH_USER_MODEL = "account.CustomUser"

JAZZMIN_SETTINGS = {
    "site_title": "OTZ Admin Panel",
    "site_header": "OTZ Group",
    "site_brand": "OTZ Group",
    "site_logo": None,  # Add path to logo file if you have one: "images/logo.png"
    "site_logo_classes": "img-circle",
    "site_icon": None,  # Add favicon path if you have one
    "welcome_sign": "OTZ Group boshqaruv paneli",
    "copyright": "OTZ Group",
    "user_avatar": None,
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "auth.user": "collapsible",
        "auth.group": "vertical_tabs",
    },
    "language_chooser": False,
    "use_theme_switcher": False,  # <-- Qo‘shing!
}


MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",  # Add CORS middleware (should be early)
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "core.middleware.RequestLoggingMiddleware",  # Custom middleware for logging
]

ROOT_URLCONF = "core.urls"

# Security settings - moved outside of DEBUG condition for better organization
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# CORS and CSRF settings
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = DEBUG  # Only allow all origins in development

if DEBUG:
    # Development settings
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8010",
        "http://127.0.0.1:8010",
    ]

    CSRF_TRUSTED_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:8010",
        "http://127.0.0.1:8010",
    ]
else:
    # Production settings
    CORS_ALLOW_ALL_ORIGINS = False
    CORS_ALLOWED_ORIGINS = [
        "https://otz-group.uz",
        "https://www.otz-group.uz",
    ]
    CSRF_TRUSTED_ORIGINS = [
        "https://otz-group.uz",
        "https://www.otz-group.uz",
    ]

    # SSL Security settings (only in production)
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Additional security settings
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"
    SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = "Lax"

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(message)s"},
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
        },
    },
    "loggers": {
        "request_logger": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# JWT Settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "VERIFYING_KEY": None,
    "AUDIENCE": None,
    "ISSUER": None,
    "JWK_URL": None,
    "LEEWAY": 0,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "USER_AUTHENTICATION_RULE": "rest_framework_simplejwt.authentication.default_user_authentication_rule",
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
    "TOKEN_TYPE_CLAIM": "token_type",
    "TOKEN_USER_CLASS": "rest_framework_simplejwt.models.TokenUser",
    "JTI_CLAIM": "jti",
    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=5),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=1),
}

# Swagger settings
SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT authorization header using the Bearer scheme. Example: 'Bearer {token}'",
        }
    },
    "USE_SESSION_AUTH": False,
    "LOGIN_URL": None,
    "LOGOUT_URL": None,
    "DOC_EXPANSION": "none",
    "APIS_SORTER": "alpha",
    "OPERATIONS_SORTER": "alpha",
    "TAGS_SORTER": "alpha",
    "DEEP_LINKING": True,
    "SHOW_EXTENSIONS": True,
    "SHOW_COMMON_EXTENSIONS": True,
}

REDOC_SETTINGS = {
    "LAZY_RENDERING": False,
}

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # Add templates directory
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
            ],
        },
    },
]

WSGI_APPLICATION = "core.wsgi.application"

# Database configuration
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST", default="db"),  # Default to 'db' for Docker
        "PORT": config("DB_PORT", default="5432"),
        "CONN_MAX_AGE": 60,  # Connection pooling
        "OPTIONS": {
            "connect_timeout": 10,
        },
    }
}


# REST Framework Configuration
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.FormParser",
        "rest_framework.parsers.MultiPartParser",
    ],
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "100/hour",
        "user": "1000/hour",
    },
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

# Add browsable API renderer for development
if DEBUG:
    REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"].append(
        "rest_framework.renderers.BrowsableAPIRenderer"
    )

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {
            "min_length": 8,
        },
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Internationalization
LANGUAGE_CODE = "uz"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"
STATIC_ROOT = str(BASE_DIR.joinpath("staticfiles"))  # Bu saqlansin

# WhiteNoise uchun eng oddiy sozlama (manifest fayllarisiz)
STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"  # Manifest versiyasiga qaraganda oddiyroq

# Agar Django admin static fayllari ishlamasa, qo'shimcha sozlama
WHITENOISE_AUTOREFRESH = True  # DEBUG=False bo'lganda ham static fayllarni yangilash


# Media files
MEDIA_URL = "media/"
MEDIA_ROOT = str(BASE_DIR.joinpath("media"))

# File Upload Settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_MEMORY_SIZE = 5242880  # 5MB
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

#
# Session Configuration
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
SESSION_COOKIE_AGE = 1209600  # 2 weeks


# Default Auto Field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Phone Number Configuration
PHONENUMBER_DEFAULT_REGION = "UZ"
PHONENUMBER_DB_FORMAT = "E164"

# Additional Security Settings
if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = "SAMEORIGIN"

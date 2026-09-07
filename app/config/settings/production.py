import os
from .rest_framework_conf import *
from .db_conf import DATABASES
from .meddleware_conf import MIDDLEWARE
from .apps_conf import INSTALLED_APPS
from .email_conf import MAILERS

from .paths import BASE_DIR

from dotenv import load_dotenv
load_dotenv()


SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', )

DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '').split(',')

# DATABASE_ROUTERS = [
#     "config.settings.router.DatabaseRouter",
# ]

WSGI_APPLICATION = 'config.wsgi.application'


ROOT_URLCONF = 'config.urls.urls'

AUTH_USER_MODEL = "accounts.UserModel"

LANGUAGE_CODE = 'fa-ir'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = True

USE_TZ = True

STATIC_URL = "/assets/static/"
STATIC_ROOT = BASE_DIR.parent / "volumes" / "assets" / "static/"

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.parent / 'volumes' / 'media'


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": os.environ["REDIS_URL"],
    }
}

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_HTTPONLY = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_AGE = 86400  # 24 hours in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_SAVE_EVERY_REQUEST = True
# SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
# SECURE_SSL_REDIRECT = True

# Maximum request body size (500 MB)
DATA_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024

# Maximum size of uploaded file kept in memory (500 MB)
FILE_UPLOAD_MAX_MEMORY_SIZE = 500 * 1024 * 1024


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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



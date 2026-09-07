import os


# ============================================================
# REDIS
# ============================================================

REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = os.environ.get("REDIS_PORT", "6379")
REDIS_PASSWORD = os.environ["REDIS_PASSWORD"]


REDIS_URL = (
    f"redis://:{REDIS_PASSWORD}"
    f"@{REDIS_HOST}:{REDIS_PORT}/0"
)


# ============================================================
# DJANGO CACHE
# ============================================================

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "veloshop",
        "TIMEOUT": 60 * 5,
    }
}


# ============================================================
# CACHE VERSIONS
# ============================================================

PRODUCT_CACHE_VERSION_KEY = "products:cache:version"
CATEGORY_CACHE_VERSION_KEY = "categories:cache:version"
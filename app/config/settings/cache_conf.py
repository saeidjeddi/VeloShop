# CACHES = {
#     "default": {
#         "BACKEND": "django.core.cache.backends.redis.RedisCache",
#         "LOCATION": os.environ["REDIS_URL"],
#     }
# }

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://redis:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "veloshop",
        "TIMEOUT": 60 * 5,
    }
}


PRODUCT_CACHE_VERSION_KEY = "products:cache:version"

CATEGORY_CACHE_VERSION_KEY = "categories:cache:version"
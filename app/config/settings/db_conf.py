import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",

        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),

        "HOST": os.environ.get("DB_HOST", "pgbouncer"),
        "PORT": os.environ.get("DB_PORT", "5432"),

        # PgBouncer transaction pooling
        "CONN_MAX_AGE": 0,
    },
}
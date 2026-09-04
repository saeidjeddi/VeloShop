import os
from dotenv import load_dotenv

load_dotenv()

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_PRIMARY_HOST"],
        "PORT": os.environ.get("DB_PRIMARY_PORT", "5432"),
        "CONN_MAX_AGE": 0,
    },

    "replica": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "HOST": os.environ["DB_REPLICA_HOST"],
        "PORT": os.environ.get("DB_REPLICA_PORT", "5432"),
        "CONN_MAX_AGE": 0,
    },
}
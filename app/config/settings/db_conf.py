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

        # PgBouncer خودش pooling انجام می‌دهد
        "CONN_MAX_AGE": 0,
    },
}
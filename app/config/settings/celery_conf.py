import os
from dotenv import load_dotenv

load_dotenv()
from kombu import Queue


RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

CELERY_BROKER_URL = (
    f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq:5672//"
)


CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"

CELERY_TIMEZONE = "Asia/Tehran"
CELERY_ENABLE_UTC = True



CELERY_BEAT_SCHEDULE = {
    "update-products-every-5-minutes": {
        "task": "products.tasks.update_products",
        "schedule": 30.0,
    },
}
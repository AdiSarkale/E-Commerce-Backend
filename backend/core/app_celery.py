from celery import Celery

celery_app = Celery(
    "ecommerce",
    broker="redis://redis-main:6379/0",
    backend="redis://redis-main:6379/0"
)

from tasks import email_task

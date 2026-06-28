from core.app_celery import celery_app
from services.email import EmailService
import asyncio


@celery_app.task
def send_order_confirmation(
    email: str,
    order_id: int
):
    asyncio.run(
        EmailService.send_mail(
            recipients=[email],
            subject='Thank You for ordering',
            body=f'<h1>ORDER ID: {order_id}</h1>'
            ))



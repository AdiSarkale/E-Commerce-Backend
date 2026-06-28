from core.app_celery import celery_app

from services.email import EmailService

import asyncio


@celery_app.task
def send_welcome_email(
    email: str
):
   asyncio.run(
       EmailService.send_mail(recipients=[email],
                              subject='Welcome',
                              body='<h1> Welcome To Panda Store </h1>'
                              ))


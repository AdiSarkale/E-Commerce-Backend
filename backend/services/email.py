from fastapi_mail import FastMail, MessageSchema
from core.mail import conf


class EmailService:

    @staticmethod
    async def send_mail(
        recipients: list[str],
        subject: str,
        body: str):

        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype='html')

        fm = FastMail(conf)


        await fm.send_message(message)



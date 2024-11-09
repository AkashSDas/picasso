from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from pydantic import EmailStr

from app.core import log, settings

conf = ConnectionConfig(
    MAIL_USERNAME=settings.mail_username,
    MAIL_PASSWORD=settings.mail_password,
    MAIL_FROM=settings.mail_from,
    MAIL_PORT=settings.mail_port,
    MAIL_SERVER=settings.mail_server,
    MAIL_STARTTLS=settings.mail_tls,
    MAIL_SSL_TLS=settings.mail_ssl,
    USE_CREDENTIALS=settings.mail_use_credentials,
)


class EmailManager:
    @classmethod
    async def send_magic_link(cls, email: EmailStr, token: str) -> None:
        try:
            log.info(f"Sending magic link email to {email}. Token: {token}")

            magic_link = f"{settings.frontend_url}/login/{token}"

            html_template = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Magic Login Link</title>
            </head>
            <body>
                <p>Hello,</p>
                <p>Click the link below to log in: </p>
                <a href="{magic_link}">Login Link</a>
                <p>If you did not request this link, please ignore this email.</p>
            </body>
            </html>
            """

            msg = MessageSchema(
                subject="Your Magic Login Link",
                recipients=[email],
                body=html_template,
                subtype=MessageType.html,
            )

            fm = FastMail(conf)
            await fm.send_message(msg)
        except Exception as e:
            log.error(f"Failed to send magic link email: {e}")


email = EmailManager()

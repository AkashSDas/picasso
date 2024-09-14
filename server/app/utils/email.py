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


class EmailUtils:
    @classmethod
    async def send_magic_link(cls, email: EmailStr, token: str, base_url: str) -> None:
        try:
            log.info(f"Sending magic link email to {email}. Token: {token}")

            magic_link = f"{base_url}/api/auth/verify?token={token}"
            msg = MessageSchema(
                subject="Your Magic Login Link",
                recipients=[email],
                body=f"Click the link to login: {magic_link}",
                subtype=MessageType.html,
            )

            fm = FastMail(conf)
            await fm.send_message(msg)
        except Exception as e:
            log.error(f"Failed to send magic link email: {e}")


email = EmailUtils()

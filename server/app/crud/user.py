from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import utils
from app.core import log
from app.core.exceptions import InternalServerError
from app.db.models import MagicLink, User


class UserCRUD:
    @staticmethod
    async def check_email_exist(db: AsyncSession, email: str) -> bool:
        stmt = select(1).where(User.email == email).limit(1)
        result = await db.scalar(stmt)
        return result is not None

    @staticmethod
    async def create(db: AsyncSession, user: User) -> tuple[User, str]:
        try:
            db.add(user)

            token, hashed = utils.auth.create_magic_link_token()
            expires_at = datetime.now(UTC) + timedelta(minutes=15)
            magic_link = MagicLink(
                unhashed_token=hashed, expires_at=expires_at, user=user
            )
            db.add(magic_link)

            await db.commit()
            await db.refresh(user)

            return user, token
        except SQLAlchemyError as e:
            log.error(f"Failed to create user account: {e}")
            await db.rollback()
            raise InternalServerError()
        except Exception as e:
            log.error(f"Failed to create user account: {e}")
            await db.rollback()
            raise InternalServerError()


user = UserCRUD()

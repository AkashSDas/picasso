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
    async def get(db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        result = await db.execute(stmt)
        return result.scalar()

    @staticmethod
    async def upsert_magic_link(db: AsyncSession, user: User) -> str:
        """Insert or update magic link record which is linked to user."""

        token, hashed = utils.auth.create_magic_link_token()
        expires_at = datetime.now(UTC) + timedelta(minutes=15)

        result = await db.execute(
            select(MagicLink).where(MagicLink.user_id == user.id).limit(1)
        )
        magic_link = result.scalar()

        if magic_link is None:
            # Create a new magic link
            instance = MagicLink(unhashed_token=token, expires_at=expires_at, user=user)
            db.add(instance)
            await db.commit()
        else:
            magic_link.expires_at = expires_at
            magic_link.unhashed_token = token
            await db.commit()

        return hashed

    @staticmethod
    async def create(db: AsyncSession, user: User) -> tuple[User, str]:
        try:
            db.add(user)

            token, hashed = utils.auth.create_magic_link_token()
            expires_at = datetime.now(UTC) + timedelta(minutes=15)
            instance = MagicLink(unhashed_token=token, expires_at=expires_at, user=user)
            db.add(instance)

            await db.commit()
            await db.refresh(user)

            return user, hashed
        except SQLAlchemyError as e:
            log.error(f"Failed to create user account: {e}")
            await db.rollback()
            raise InternalServerError()
        except Exception as e:
            log.error(f"Failed to create user account: {e}")
            await db.rollback()
            raise InternalServerError()


user = UserCRUD()

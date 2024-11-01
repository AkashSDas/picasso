from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app import utils
from app.core import log
from app.core.exceptions import InternalServerError
from app.db.models import MagicLink, User


class UserCRUD:
    @staticmethod
    async def exists_by_email(db: AsyncSession, email: str) -> bool:
        stmt = select(1).where(User.email == email).limit(1)
        result = await db.scalar(stmt)
        return result is not None

    @staticmethod
    async def exists_by_username(db: AsyncSession, username: str) -> bool:
        stmt = select(1).where(User.username == username).limit(1)
        result = await db.scalar(stmt)
        return result is not None

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
            raise InternalServerError() from e
        except Exception as e:
            log.error(f"Failed to create user account: {e}")
            await db.rollback()
            raise InternalServerError() from e

    @staticmethod
    async def get_by_public_user_id(
        db: AsyncSession,
        public_user_id: str | UUID,
    ) -> User | None:
        stmt = select(User).where(User.public_user_id == public_user_id).limit(1)
        result = await db.execute(stmt)
        return result.scalar()

    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email).limit(1)
        result = await db.execute(stmt)
        return result.scalar()


user = UserCRUD()

from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import utils
from app.core import log
from app.db.models import MagicLink, User


class MagicLinkCRUD:
    @staticmethod
    async def get_by_hashed_token(
        db: AsyncSession,
        token: str,
    ) -> tuple[MagicLink, UUID] | None:
        unhashed_token = utils.auth.unhash_token(token)
        now = datetime.now(UTC)

        result = await db.execute(
            select(MagicLink, User.public_user_id)
            .join(User, User.id == MagicLink.user_id)
            .where(
                MagicLink.unhashed_token == unhashed_token,
                MagicLink.expires_at.isnot(None),
                MagicLink.expires_at <= now,
            )
            .limit(1)
        )

        return result.scalar()

    @staticmethod
    async def unset_magic_link(db: AsyncSession, magic_link: MagicLink) -> None:
        log.info(f"Unset magic link login for user id ({magic_link.user_id})")

        magic_link.unhashed_token = None
        magic_link.expires_at = None

        db.add(magic_link)
        await db.commit()

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


magic_link = MagicLinkCRUD()

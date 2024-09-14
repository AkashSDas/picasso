from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User


class UserCRUD:
    @staticmethod
    async def check_email_exist(db: AsyncSession, email: str) -> bool:
        stmt = select(1).where(User.email == email).limit(1)
        result = await db.scalar(stmt)
        return result is not None

    @staticmethod
    async def create(db: AsyncSession, user: User) -> User:
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user


user = UserCRUD()

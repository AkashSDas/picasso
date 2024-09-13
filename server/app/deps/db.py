from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import AsyncDbSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDbSession() as session:
        yield session

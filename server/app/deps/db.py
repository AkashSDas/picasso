from typing import Annotated, AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import AsyncDbSession


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncDbSession() as session:
        yield session


db_dependency = Annotated[AsyncSession, Depends(get_db)]

from uuid import UUID

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import StyleFilter
from app.utils import FilterUploadResult


class StyleFilterCRUD:
    @staticmethod
    async def create_many(
        db: AsyncSession,
        style_filters: list[FilterUploadResult],
        author_id: int,
    ) -> list[StyleFilter]:
        instances: list[StyleFilter] = []

        for filter in style_filters:
            instance = StyleFilter.from_upload_result(filter, author_id)
            instances.append(instance)
            db.add(instance)

        await db.commit()

        for instance in instances:
            await db.refresh(instance)

        return instances

    @staticmethod
    async def get_many(
        db: AsyncSession,
        filter_public_ids: list[UUID],
    ) -> list[StyleFilter]:
        result = await db.execute(
            select(StyleFilter).where(
                StyleFilter.public_filter_id.in_(filter_public_ids)
            )
        )

        return list(result.scalars())

    @staticmethod
    async def delete_many(db: AsyncSession, filter_ids: list[int]) -> None:
        await db.execute(
            delete(StyleFilter).where(StyleFilter.id.in_(filter_ids)),
        )


style_filters = StyleFilterCRUD()

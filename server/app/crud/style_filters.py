from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import StyleFilter
from app.utils import FilterUploadResult


class StyleFilterCRUD:
    @staticmethod
    async def create_filters(
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


style_filters = StyleFilterCRUD()

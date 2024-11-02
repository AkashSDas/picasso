from uuid import UUID

from sqlalchemy import case, delete, desc, func, literal, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import StyleFilter, User
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
    async def get_many_by_ids(
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
    async def get_many(
        db: AsyncSession,
        *,
        author_id: UUID | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> tuple[list[StyleFilter], int]:
        stmt = select(StyleFilter)
        total_stmt = select(func.count()).select_from(StyleFilter)

        if author_id is not None:
            stmt = stmt.join(User).where(User.public_user_id == author_id)
            total_stmt = total_stmt.join(User).where(User.public_user_id == author_id)

        result = await db.execute(
            stmt.limit(limit).offset(offset).order_by(desc(StyleFilter.created_at))
        )

        total = await db.execute(total_stmt)

        return list(result.scalars()), total.scalar() or 0

    @staticmethod
    async def get_report_count(db: AsyncSession, filter_public_id: UUID) -> int | None:
        result = await db.execute(
            select(StyleFilter.report_count)
            .where(StyleFilter.public_filter_id == filter_public_id)
            .limit(1)
        )

        return result.scalar()

    @staticmethod
    async def change_report_count(
        db: AsyncSession,
        filter_public_id: UUID,
        is_increment: bool,
        is_banned: bool,
    ) -> None:
        await db.execute(
            update(StyleFilter)
            .where(StyleFilter.public_filter_id == filter_public_id)
            .values(
                report_count=case(
                    (literal(is_increment), StyleFilter.report_count + 1),
                    else_=StyleFilter.report_count - 1,
                ),
                is_banned=case((literal(is_banned), True), else_=False),
            )
        )

        await db.commit()

    @staticmethod
    async def delete_many(db: AsyncSession, filter_ids: list[int]) -> None:
        await db.execute(
            delete(StyleFilter).where(StyleFilter.id.in_(filter_ids)),
        )


style_filter = StyleFilterCRUD()

from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import Boolean, CheckConstraint, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseDbModel, make_column_unupdateable
from app.db.models.user import User

if TYPE_CHECKING:
    from app.utils import FilterUploadResult


class StyleFilter(BaseDbModel):
    __tablename__ = "style_filters"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    # Set a default value using SQL expression, e.g., using a database
    # function or sequence. This will be public facing filter id
    public_filter_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4(),
        unique=True,
        index=True,
    )

    base_img_url: Mapped[str] = mapped_column(String(2048))
    blur_img_url: Mapped[str] = mapped_column(String(2048))
    small_img_url: Mapped[str] = mapped_column(String(2048))

    # ID provided by the storage service, which can be used to delete it. In case
    # we give img url, like paste it, that time we won't have img id and hence optional
    img_id: Mapped[str | None] = mapped_column(String(32))

    # Is the image uploaded by an external user or the platform itself
    is_official: Mapped[bool] = mapped_column(Boolean, default=False)

    is_banned: Mapped[bool] = mapped_column(Boolean, default=False)
    report_count: Mapped[int] = mapped_column(
        Integer,
        CheckConstraint("report_count >= 0"),
        default=0,
    )

    # Don't delete filter if the user is deleted, just set the foreign key to NULL
    author_id: Mapped[int | None] = mapped_column(
        ForeignKey(User.id, ondelete="SET NULL"),
        index=True,
    )

    # User one-to-many relationship with StyleFilter
    author: Mapped["User"] = relationship(
        back_populates="style_filters",
        #
        # When a StyleFilter is loaded, load its author (if there) in a single
        # JOIN query. This will use single query
        lazy="joined",
        #
        # `passive_deletes="all"` tells SQLAlchemy not to process related objects when
        # deleting a parent object
        # https://stackoverflow.com/questions/53508334/how-do-i-define-sqlalchemy-fks-and-relationships-to-allow-the-database-to-cascad
        passive_deletes="all",
    )

    # Ensure that public_user_id cannot be modified after creation
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if "public_filter_id" in kwargs:
            raise ValueError("public_filter_id cannot be set manually")

    def __str__(self) -> str:
        return (
            f"StyleFilter({self.id}, {self.public_filter_id}, {self.img_id}, "
            f"{self.author_id})"
        )

    @classmethod
    def from_upload_result(cls, upload_result: "FilterUploadResult") -> "StyleFilter":
        return cls(
            base_img_url=upload_result.base_img_url,
            blur_img_url=upload_result.blur_img_url,
            small_img_url=upload_result.small_img_url,
            img_id=upload_result.img_id,
        )


make_column_unupdateable(StyleFilter.public_filter_id)

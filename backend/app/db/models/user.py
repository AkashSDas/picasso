from datetime import datetime
from typing import TYPE_CHECKING
from uuid import uuid4

from sqlalchemy import ARRAY, DateTime, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import schemas
from app.db.base import BaseDbModel, make_column_unupdateable

if TYPE_CHECKING:
    from app.db.models import MagicLink, StyleFilter


class User(BaseDbModel):
    __tablename__ = "users"

    # ===========================
    # Columns
    # ===========================

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    # Set a default value using SQL expression, e.g., using a database
    # function or sequence. This will be public facing user id
    public_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        index=True,
    )

    username: Mapped[str] = mapped_column(String(255), index=True, unique=True)
    email: Mapped[str] = mapped_column(String(255), index=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_banned: Mapped[bool] = mapped_column(default=False)

    profile_pic_url: Mapped[str] = mapped_column(String(255))

    # ID for profile pic management (for use with S3 or other storage)
    profile_pic_id: Mapped[str | None] = mapped_column(String(32))

    reported_filter_ids: Mapped[list[int]] = mapped_column(
        ARRAY(Integer),
        default=list,
        server_default="{}",
        nullable=False,
    )

    # Automatically set by the DB when the record is created
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),  # Automatically set on record creation
    )

    # Automatically updated by the DB when the record is updated
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=func.now(),
        onupdate=func.now(),  # Automatically updated on any change
    )

    # ===========================
    # Relationships
    # ===========================

    # One-to-one relationship with MagicLink
    magic_link: Mapped["MagicLink"] = relationship(
        back_populates="user",
        uselist=False,
        lazy="noload",
    )

    # One-to-many relationships with StyleFilter
    style_filters: Mapped["StyleFilter"] = relationship(
        back_populates="author",
        # Performs an immediate join using SQL's JOIN clause when the parent object
        # is loaded, so both the parent and related objects are fetched in one query.
        lazy="joined",
    )

    # ===========================
    # Methods
    # ===========================

    # Ensure that public_user_id cannot be modified after creation
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        if "public_user_id" in kwargs:
            raise ValueError("public_user_id cannot be set manually")

    def __str__(self) -> str:
        return f"User({self.id}, {self.public_user_id}, {self.username})"

    @classmethod
    def from_schema(
        cls,
        schema: schemas.http.EmailSignupIn,
        profile_pic_url: str,
    ) -> "User":
        return cls(
            email=schema.email,
            username=schema.username,
            profile_pic_url=profile_pic_url,
        )

    def to_schema(self) -> schemas.User:
        return schemas.User.model_validate(
            {
                "user_id": self.public_user_id,
                "profile_pic_url": self.profile_pic_url,
                "email": self.email,
                "username": self.username,
            }
        )


make_column_unupdateable(User.public_user_id)
make_column_unupdateable(User.created_at)

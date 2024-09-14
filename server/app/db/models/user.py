from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseDbModel, make_column_unupdateable
from app.schemas.auth import SignupIn


class User(BaseDbModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    # Set a default value using SQL expression, e.g., using a database
    # function or sequence
    public_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4(),
        unique=True,
        index=True,
    )

    email: Mapped[str] = mapped_column(String(255), index=True)

    is_active: Mapped[bool] = mapped_column(default=True)
    is_banned: Mapped[bool] = mapped_column(default=False)

    profile_pic_url: Mapped[str] = mapped_column(String(255))

    # ID for profile pic management (for use with S3 or other storage)
    profile_pic_id: Mapped[str | None] = mapped_column(String(32))

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

    # Ensure that public_user_id cannot be modified after creation
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if "public_user_id" in kwargs:
            raise ValueError("public_user_id cannot be set manually")

    @classmethod
    def from_schema(cls, schema: SignupIn) -> "User":
        return cls(
            email=schema.email,
            profile_pic_url="/static/images/default-profile.jpg",
        )


make_column_unupdateable(User.public_user_id)
make_column_unupdateable(User.created_at)

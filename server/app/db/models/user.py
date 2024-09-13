from datetime import datetime

from sqlalchemy import DateTime, String, func, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import BaseDbModel


class User(BaseDbModel):
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True,
    )

    # Set a default value using SQL expression, e.g., using a database
    # function or sequence
    public_user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        # Assuming PostgreSQL with uuid-ossp extension
        server_default=text("uuid_generate_v4()"),
        unique=True,
    )

    is_active: Mapped[bool] = mapped_column(default=False)
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

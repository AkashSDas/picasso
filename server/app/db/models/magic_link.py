from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import BaseDbModel
from app.db.models import User


class MagicLink(BaseDbModel):
    __tablename__ = "magic_links"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    unhashed_token: Mapped[str | None] = mapped_column(String(255), index=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    # One-to-one mapping with the User model
    user_id: Mapped[int] = mapped_column(ForeignKey(User.id), unique=True, index=True)
    user: Mapped["User"] = relationship(
        back_populates="magic_link",
        cascade="delete",
        lazy="noload",
    )

    def __str__(self) -> str:
        return f"MagicLink({self.id}, {self.user_id})"

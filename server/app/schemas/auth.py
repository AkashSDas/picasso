from uuid import UUID

from pydantic import BaseModel


class AuthToken(BaseModel):
    user_id: UUID

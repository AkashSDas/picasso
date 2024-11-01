from uuid import UUID

from pydantic import BaseModel, Field


class StyleFilterDeleteQuery(BaseModel):
    """Query Pydantic model to delete multiple style filters"""

    filter_ids: list[UUID] = Field(..., alias="filterIds", min_length=1)

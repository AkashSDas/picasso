from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class StyleFilterDeleteQuery(BaseModel):
    filter_ids: list[UUID] = Field(..., alias="filterIds", min_length=1)


class ReportStyleFilterQuery(BaseModel):
    type: Literal["increment", "decrement"]


class GetStyleFiltersQuery(BaseModel):
    limit: int = Field(20, ge=0, le=100)
    offset: int = Field(0, ge=0)
    author_id: UUID | None = None

from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


class StyleFilterDeleteQuery(BaseModel):
    model_config = {"extra": "forbid"}
    filter_ids: list[UUID] = Field(..., alias="filterIds", min_length=1)


class ReportStyleFilterQuery(BaseModel):
    model_config = {"extra": "forbid"}
    type: Literal["increment", "decrement"]


class GetStyleFiltersQuery(BaseModel):
    model_config = {"extra": "forbid"}
    limit: int = Field(20, ge=0, le=100)
    offset: int = Field(0, ge=0)
    author_id: UUID | None = None
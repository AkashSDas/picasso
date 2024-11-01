from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, Field

if TYPE_CHECKING:
    from app.schemas import StyleFilter

# =============================
# Upload Style Filters
# =============================


class UploadStyleFiltersOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filters: list["StyleFilter"] = Field(..., min_length=1)


# =============================
# Report Style Filter
# =============================


class ReportStyleFilterOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    is_banned: bool = False


# =============================
# Get author's style filters
# =============================


class AuthorStyleFiltersOut(UploadStyleFiltersOut):
    total: int = Field(..., ge=0)

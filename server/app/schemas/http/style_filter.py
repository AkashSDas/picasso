from pydantic import BaseModel, ConfigDict, Field

from app.schemas import StyleFilter

# =============================
# Upload Style Filters
# =============================


class UploadStyleFiltersOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    filters: list[StyleFilter] = Field(..., min_length=1)

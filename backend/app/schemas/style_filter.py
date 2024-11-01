from pydantic import UUID4, AnyHttpUrl, BaseModel, ConfigDict, Field


class StyleFilter(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        from_attributes=True,
    )

    filter_id: UUID4 = Field(..., alias="filterId")
    author_id: UUID4 = Field(..., alias="authorId")

    img_id: str = Field(..., alias="imgId")
    img_url: AnyHttpUrl = Field(..., alias="imgURL")
    blur_img_url: AnyHttpUrl = Field(..., alias="blurImgURL")
    small_img_url: AnyHttpUrl = Field(..., alias="smallImgURL")

    is_official: bool = Field(..., alias="isOfficial")
    is_banned: bool = Field(..., alias="isBanned")
    report_count: int = Field(..., alias="reportCount", ge=0)

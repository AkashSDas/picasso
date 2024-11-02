from pydantic import UUID4, AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        populate_by_name=True,
        from_attributes=True,
    )

    user_id: UUID4 = Field(..., alias="userId")
    username: str = Field(..., min_length=3, max_length=255)
    email: EmailStr
    profile_pic_url: AnyHttpUrl = Field(..., alias="profilePicURL")

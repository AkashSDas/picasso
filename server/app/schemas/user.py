from pydantic import UUID4, AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field


class User(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    user_id: UUID4 = Field(..., alias="userId")
    email: EmailStr
    profile_pic_url: AnyHttpUrl = Field(..., alias="profilePicURL")

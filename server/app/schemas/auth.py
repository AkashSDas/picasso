from pydantic import BaseModel, ConfigDict, EmailStr, Field


class SignupIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class SignupOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    detail: str


class SignupEmailAlreadyExistOut(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    detail: str
    user_email: EmailStr = Field(..., alias="userEmail")


class AuthToken(BaseModel):
    email: EmailStr

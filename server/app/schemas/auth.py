from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas import User


class AuthToken(BaseModel):
    user_id: int


# =============================
# Signup
# =============================


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


# =============================
# Login
# =============================


class LoginIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class LoginOut(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    detail: str


class CompleteMagicLinkOut(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    access_token: str = Field(..., alias="accessToken")
    user: User


class RefreshAccessTokenOut(CompleteMagicLinkOut):
    pass

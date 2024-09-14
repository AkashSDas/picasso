from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, EmailStr, Field

if TYPE_CHECKING:
    from app import schemas


class AuthToken(BaseModel):
    email: EmailStr


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


class CompleteMagicLinkLoginOut(BaseModel):
    model_config = ConfigDict(extra="forbid", populate_by_name=True)
    access_token: str = Field(..., alias="accessToken")
    user: "schemas.User"

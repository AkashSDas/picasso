from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.schemas import User

# =============================
# Email Signup
# =============================


class EmailSignupIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=255)


class EmailSignupOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str


# =============================
# Email Login
# =============================


class EmailLoginIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    email: EmailStr


class EmailLoginOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    message: str


# =============================
# Complete Email Login
# =============================


class CompleteEmailLoginOut(BaseModel):
    model_config = ConfigDict(extra="forbid")
    access_token: str = Field(..., alias="accessToken")
    user: User


class RefreshAccessTokenOut(CompleteEmailLoginOut):
    pass

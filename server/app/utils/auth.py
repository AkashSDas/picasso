import hashlib
import secrets
from datetime import UTC, datetime, timedelta
from typing import Literal, TypedDict

from jose import JWTError, jwt

from app.core import settings
from app.core.exceptions import UnauthorizedError
from app.schemas.auth import AuthToken


class AccessTokenPayload(TypedDict):
    sub: int


class AuthUtils:
    @classmethod
    def create_access_token(cls, data: AccessTokenPayload) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.auth_access_token_expire
        )

        return jwt.encode(
            {**to_encode, "exp": expire},
            settings.auth_jwt_secret_key,
            algorithm=settings.auth_jwt_algorithm,
        )

    @classmethod
    def create_refresh_token(cls, data: AccessTokenPayload) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(
            minutes=settings.auth_refresh_token_expire
        )

        return jwt.encode(
            {**to_encode, "exp": expire},
            settings.auth_jwt_secret_key,
            algorithm=settings.auth_jwt_algorithm,
        )

    @classmethod
    def verfiy_token(cls, token: str) -> AuthToken | None:
        try:
            payload = jwt.decode(
                token,
                settings.auth_jwt_secret_key,
                algorithms=[settings.auth_jwt_algorithm],
            )

            email = payload.get("sub")
            if email is None:
                raise UnauthorizedError()

            return AuthToken(email=email)
        except JWTError:
            raise UnauthorizedError()

    @classmethod
    def generate_token(cls, length: Literal[16, 32, 64]) -> str:
        return secrets.token_hex(length)

    @classmethod
    def hash_token(cls, token: str) -> str:
        return hashlib.sha256(token.encode("utf-8")).hexdigest()

    @classmethod
    def create_magic_link_token(cls) -> tuple[str, str]:
        token = cls.generate_token(64)
        hashed_token = cls.hash_token(token)

        return token, hashed_token


auth = AuthUtils()

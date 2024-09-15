import secrets
from datetime import UTC, datetime, timedelta
from typing import Literal, TypedDict

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud
from app.core import log, settings
from app.core.exceptions import UnauthorizedError
from app.db.models.user import User
from app.schemas.auth import AuthToken


class AccessTokenPayload(TypedDict):
    sub: str  # subject must be a string


class AuthUtils:
    cipher_suite = Fernet(settings.auth_magic_token_hash_key)

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
    async def decode_access_token(cls, db: AsyncSession, token: str) -> User:
        try:
            payload = jwt.decode(
                token,
                settings.auth_jwt_secret_key,
                algorithms=[settings.auth_jwt_algorithm],
            )

            user_id = payload.get("sub")
            if user_id is None:
                raise UnauthorizedError()

            user = await crud.user.get_by_id(db, int(user_id))

            if not user:
                raise UnauthorizedError()

            return user
        except JWTError as e:
            log.error(f"Failed to decode access token: {token}, error: {e}")
            raise UnauthorizedError()

    @classmethod
    def create_refresh_token(cls, data: AccessTokenPayload) -> str:
        to_encode = data.copy()
        expire = datetime.now(UTC) + timedelta(days=settings.auth_refresh_token_expire)

        return jwt.encode(
            {**to_encode, "exp": expire},
            settings.auth_jwt_secret_key,
            algorithm=settings.auth_jwt_algorithm,
        )

    @classmethod
    def verfiy_jwt_token(cls, token: str) -> AuthToken | None:
        try:
            payload = jwt.decode(
                token,
                settings.auth_jwt_secret_key,
                algorithms=[settings.auth_jwt_algorithm],
            )

            user_id = payload.get("sub")

            if user_id is None:
                log.error(f"Failed to decode JWT token: {token}")
                raise UnauthorizedError(
                    headers={"X-Auth-Error": "Invalid JWT token payload"}
                )

            return AuthToken(user_id=int(user_id))
        except JWTError as e:
            log.error(f"Failed to decode JWT token: {token}, error: {e}")
            raise UnauthorizedError(
                headers={"X-Auth-Error": "Failed to decode JWT token"}
            )

    @classmethod
    def generate_token(cls, length: Literal[16, 32, 64]) -> str:
        return secrets.token_hex(length)

    @classmethod
    def hash_token(cls, token: str) -> str:
        encrypted_token = cls.cipher_suite.encrypt(token.encode("utf-8"))
        return encrypted_token.decode("utf-8")

    @classmethod
    def unhash_token(cls, hashed_token: str) -> str:
        decrypted_token = cls.cipher_suite.decrypt(hashed_token.encode("utf-8"))
        return decrypted_token.decode("utf-8")

    @classmethod
    def create_magic_link_token(cls) -> tuple[str, str]:
        token = cls.generate_token(64)
        hashed_token = cls.hash_token(token)

        return token, hashed_token


auth = AuthUtils()

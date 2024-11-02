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

JWTKey = Literal["access", "refresh"]


class AccessTokenPayload(TypedDict):
    sub: str  # subject must be a string


class RefreshTokenPayload(AccessTokenPayload):
    pass


class AuthManager:
    cipher_suite = Fernet(settings.auth_crypto_hash_key)

    # ==================================
    # JWT
    # ==================================

    @classmethod
    def create_access_token(cls, data: AccessTokenPayload) -> str:
        to_encode = data.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(milliseconds=settings.auth_access_token_expire_in_ms)

        return jwt.encode(
            {**to_encode, "exp": expire},
            settings.auth_access_token_secret_key,
            algorithm=settings.auth_jwt_algorithm,
        )

    @classmethod
    def create_refresh_token(cls, data: AccessTokenPayload) -> str:
        to_encode = data.copy()
        now = datetime.now(UTC)
        expire = now + timedelta(milliseconds=settings.auth_refresh_token_expire_in_ms)

        return jwt.encode(
            {**to_encode, "exp": expire},
            settings.auth_refresh_token_secret_key,
            algorithm=settings.auth_jwt_algorithm,
        )

    @classmethod
    async def decode_jwt_token(cls, db: AsyncSession, token: str, key: JWTKey) -> User:
        """Decode refresh/access tokens as they both use same secret key"""

        try:
            _key = settings.auth_access_token_secret_key
            if key == "refresh":
                _key = settings.auth_refresh_token_secret_key

            payload = jwt.decode(token, _key, algorithms=[settings.auth_jwt_algorithm])

            user_id = payload.get("sub")
            if not isinstance(user_id, str):
                raise UnauthorizedError()

            user = await crud.user.get_by_public_user_id(db, user_id)

            if not user:
                raise UnauthorizedError()

            return user
        except JWTError as e:
            log.error(f"Failed to decode access token: {token}, error: {e}")
            raise UnauthorizedError() from e

    @classmethod
    def verify_jwt_token(cls, token: str, key: JWTKey) -> AuthToken | None:
        try:
            _key = settings.auth_access_token_secret_key
            if key == "refresh":
                _key = settings.auth_refresh_token_secret_key

            payload = jwt.decode(token, _key, algorithms=[settings.auth_jwt_algorithm])

            user_id = payload.get("sub")

            if user_id is None:
                log.error(f"Failed to decode JWT token: {token}")
                raise UnauthorizedError()

            return AuthToken(user_id=user_id)
        except JWTError as e:
            log.error(f"Failed to decode JWT token: {token}, error: {e}")
            raise UnauthorizedError()

    # ==================================
    # Magic Link
    # ==================================

    @classmethod
    def create_magic_link_token(cls) -> tuple[str, str]:
        token = cls.generate_token(64)
        hashed_token = cls.hash_token(token)

        return token, hashed_token

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


auth = AuthManager()

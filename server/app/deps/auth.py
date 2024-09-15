from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from app import utils
from app.core.exceptions import UnauthorizedError
from app.db.models.user import User
from app.deps import db_dependency

security = HTTPBearer()


async def get_current_user(req: Request, db: db_dependency) -> User:
    access_token = req.headers.get("Authorization")

    if not isinstance(access_token, str):
        raise UnauthorizedError()

    access_token = access_token.replace("Bearer ", "")
    return await utils.auth.decode_access_token(db, access_token)


current_user_dependency = Annotated[User, Depends(get_current_user)]

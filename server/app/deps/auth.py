from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import HTTPBearer

from app import utils
from app.core.exceptions import UnauthorizedError
from app.db.models.user import User
from app.deps import db_dep

security = HTTPBearer()


async def current_user(req: Request, db: db_dep) -> User:
    access_token = req.headers.get("Authorization")

    if not isinstance(access_token, str):
        raise UnauthorizedError()

    access_token = access_token.replace("Bearer ", "")
    return await utils.auth.decode_jwt_token(db, access_token, "access")


current_user_dep = Annotated[User, Depends(current_user)]

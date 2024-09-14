from typing import Annotated

from fastapi import APIRouter, Body, status

from app import crud, schemas
from app.core.exceptions import BadRequestError
from app.db.models.user import User
from app.deps.db import db_dependency

router = APIRouter()


@router.post(
    "/signup/email",
    summary="Signup via email",
    responses={
        status.HTTP_201_CREATED: {"model": schemas.SignupOut},
        status.HTTP_400_BAD_REQUEST: {"model": schemas.SignupEmailAlreadyExistOut},
    },
    response_model=schemas.SignupOut,
)
async def signup_via_email(
    db: db_dependency,
    body: Annotated[schemas.SignupIn, Body()],
) -> schemas.SignupOut:
    exists = await crud.user.check_email_exist(db, body.email)

    if exists:
        raise BadRequestError("Email already used", context={"user_email": body.email})
    else:
        user = User.from_schema(body)
        user = await crud.user.create(db, user)

        return schemas.SignupOut(detail="Signup successful")

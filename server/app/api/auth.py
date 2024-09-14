from typing import Annotated, cast

from fastapi import APIRouter, BackgroundTasks, Body, Request, status
from pydantic import EmailStr

from app import crud, schemas, utils
from app.core import log
from app.core.exceptions import BadRequestError, NotFoundError
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
    req: Request,
    db: db_dependency,
    body: Annotated[schemas.SignupIn, Body()],
    background_tasks: BackgroundTasks,
) -> schemas.SignupOut:
    exists = await crud.user.check_email_exist(db, body.email)

    if exists:
        raise BadRequestError("Email already used", context={"user_email": body.email})
    else:
        user = User.from_schema(body)
        user, token = await crud.user.create(db, user)
        log.info(f"Created account for email ({user.email}). ID {user.id}")

        background_tasks.add_task(
            utils.email.send_magic_link,
            cast(EmailStr, user.email),
            token,
            str(req.base_url),
        )

        return schemas.SignupOut(detail="Magic link login sent to your email")


@router.post(
    "/login/email",
    summary="Login via email",
    responses={status.HTTP_200_OK: {"model": schemas.LoginOut}},
    response_model=schemas.LoginOut,
)
async def init_magic_link_login(
    req: Request,
    db: db_dependency,
    body: Annotated[schemas.LoginIn, Body()],
    background_tasks: BackgroundTasks,
) -> schemas.LoginOut:
    user = await crud.user.get(db, body.email)

    if not user:
        raise NotFoundError(f"User not found with email: {body.email}")
    else:
        token = await crud.user.upsert_magic_link(db, user)

        background_tasks.add_task(
            utils.email.send_magic_link,
            cast(EmailStr, user.email),
            token,
            str(req.base_url),
        )

        return schemas.LoginOut(detail="Magic link login sent to your email")

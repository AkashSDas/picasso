from typing import Annotated, cast

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Request, Response, status
from pydantic import EmailStr

from app import crud, schemas, utils
from app.core import log
from app.core.exceptions import BadRequestError, NotFoundError, UnauthorizedError
from app.db.models.user import User
from app.deps.auth import get_current_user
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
        raise BadRequestError("Email already used", context={"userEmail": body.email})
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


@router.get(
    "/login/email/{token}",
    summary="Complete magic email login",
    response_model=schemas.CompleteMagicLinkOut,
)
async def complete_magic_link_login(
    token: str,
    db: db_dependency,
    res: Response,
    background_tasks: BackgroundTasks,
) -> schemas.CompleteMagicLinkOut:
    magic_link = await crud.user.get_magic_link_by_hashed_token(db, token)

    if not magic_link:
        raise BadRequestError(detail="Magic link is invalid or expired")
    else:
        data: utils.AccessTokenPayload = {"sub": str(magic_link.user_id)}
        access_token = utils.auth.create_access_token(data)
        refresh_token = utils.auth.create_refresh_token(data)

        user = await crud.user.get_by_id(db, magic_link.id)
        if not user:
            raise NotFoundError(f"User with user id ({magic_link.id}) is not found")
        else:
            res.set_cookie(
                key="refresh_token",
                value=refresh_token,
                httponly=True,
                secure=True,
                max_age=3600,  # 1 hour
            )

            background_tasks.add_task(crud.user.unset_magic_link, db, magic_link)

            return schemas.CompleteMagicLinkOut(
                accessToken=access_token, user=user.to_schema()
            )


@router.get(
    "/refresh",
    summary="Refresh access token",
    response_model=schemas.RefreshAccessTokenOut,
)
async def refresh_access_token(
    req: Request,
    db: db_dependency,
) -> schemas.RefreshAccessTokenOut:
    refresh_token = req.cookies.get("refresh_token")
    if not refresh_token:
        log.info("Refresh token not found")
        raise UnauthorizedError()

    jwt_payload = utils.auth.verfiy_jwt_token(refresh_token)
    if not jwt_payload:
        log.info(f"Invalid JWT payload: {jwt_payload}")
        raise UnauthorizedError()

    user = await crud.user.get_by_id(db, jwt_payload.user_id)
    if not user:
        log.info(f"User not found with user id: {jwt_payload.user_id}")
        raise UnauthorizedError()

    access_token = utils.auth.create_access_token({"sub": str(user.id)})

    return schemas.RefreshAccessTokenOut(
        accessToken=access_token, user=user.to_schema()
    )


@router.get(
    "/logout",
    summary="Logout logged in user",
    dependencies=[Depends(get_current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
)
async def logout_user(res: Response) -> None:
    res.delete_cookie(key="refresh_token")

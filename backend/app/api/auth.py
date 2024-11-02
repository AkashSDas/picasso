from typing import Annotated, cast

from fastapi import APIRouter, BackgroundTasks, Body, Depends, Request, Response, status
from pydantic import EmailStr

from app import crud, schemas, utils
from app.core import log, responses, settings
from app.core.exceptions import BadRequestError, UnauthorizedError
from app.db.models.user import User
from app.deps.auth import current_user
from app.deps.db import db_dep
from app.utils.enums import Cookie

router = APIRouter()


@router.post(
    "/signup/email",
    summary=(
        "Signup using email and username. Both of them should be unique. This will "
        "send magic link for login on the registered email address"
    ),
    responses=responses.email_signup,
    response_model=responses.email_signup[status.HTTP_201_CREATED]["model"],
)
async def email_signup(
    req: Request,
    db: db_dep,
    body: Annotated[schemas.http.EmailSignupIn, Body()],
    background_tasks: BackgroundTasks,
) -> schemas.http.EmailSignupOut:
    email_exists = await crud.user.exists_by_email(db, body.email)
    username_exists = await crud.user.exists_by_username(db, body.username)

    if email_exists:
        raise BadRequestError("Email already used")
    if username_exists:
        raise BadRequestError("Username already used")

    user = User.from_schema(body, f"{req.base_url}static/images/default-profile.jpg")
    user, token = await crud.user.create(db, user)
    log.info(f"Created account for email ({user.email}) with ID {user.id}")

    background_tasks.add_task(
        utils.email.send_magic_link,
        cast(EmailStr, user.email),
        token,
        str(req.base_url),
    )

    return schemas.http.EmailSignupOut(message="Magic link login sent to your email")


@router.post(
    "/login/email",
    summary=(
        "Login using email. This will send magic send magic link for login on "
        "the registered email address"
    ),
    responses=responses.email_login,
    response_model=responses.email_login[status.HTTP_200_OK]["model"],
)
async def email_login(
    req: Request,
    db: db_dep,
    body: Annotated[schemas.http.EmailLoginIn, Body()],
    background_tasks: BackgroundTasks,
) -> schemas.http.EmailLoginOut:
    user = await crud.user.get_by_email(db, body.email)

    if not user:
        raise BadRequestError("Account doesn't exists")

    token = await crud.magic_link.upsert_magic_link(db, user)

    if settings.environment == "development":
        return schemas.http.EmailLoginOut(
            message=(f"Magic link login sent to your email. Login token: {token}"),
        )

    background_tasks.add_task(
        utils.email.send_magic_link,
        cast(EmailStr, user.email),
        token,
        str(req.base_url),
    )

    return schemas.http.EmailLoginOut(message="Magic link login sent to your email")


@router.get(
    "/login/email/{token}",
    summary=(
        "Complete magic link login and then set refresh token and sending access token"
    ),
    responses=responses.complete_email_login,
    response_model=responses.complete_email_login[status.HTTP_200_OK]["model"],
)
async def complete_email_login(
    token: str,
    db: db_dep,
    res: Response,
    background_tasks: BackgroundTasks,
) -> schemas.http.CompleteEmailLoginOut:
    result = await crud.magic_link.get_by_hashed_token(db, token)

    if result is None:
        raise BadRequestError("Magic login link is invalid or expired")

    magic_link, user_id = result

    data: utils.AccessTokenPayload = {"sub": str(user_id)}
    access_token = utils.auth.create_access_token(data)
    refresh_token = utils.auth.create_refresh_token(data)

    user = await crud.user.get_by_public_user_id(db, user_id)
    if not user:
        raise BadRequestError("Account doesn't exists")

    res.set_cookie(
        key=Cookie.REFRESH_TOKEN.value,
        value=refresh_token,
        httponly=True,
        secure=settings.environment == "production",
        max_age=settings.auth_refresh_token_expire_in_ms,
    )

    background_tasks.add_task(crud.magic_link.unset_magic_link, db, magic_link)

    return schemas.http.CompleteEmailLoginOut(
        accessToken=access_token,
        user=user.to_schema(),
    )


@router.get(
    "/refresh",
    summary="Refresh access token",
    responses=responses.refresh_access_token,
    response_model=responses.refresh_access_token[status.HTTP_200_OK]["model"],
)
async def refresh_access_token(
    req: Request,
    db: db_dep,
) -> schemas.http.RefreshAccessTokenOut:
    refresh_token = req.cookies.get(Cookie.REFRESH_TOKEN.value)
    if refresh_token is None:
        raise UnauthorizedError()

    jwt_payload = utils.auth.verify_jwt_token(refresh_token, "refresh")
    if not jwt_payload:
        raise UnauthorizedError()

    user = await crud.user.get_by_public_user_id(db, jwt_payload.user_id)
    if not user:
        raise UnauthorizedError()

    access_token = utils.auth.create_access_token({"sub": str(user.public_user_id)})

    return schemas.http.RefreshAccessTokenOut(
        accessToken=access_token,
        user=user.to_schema(),
    )


@router.get(
    "/logout",
    summary="Logout user",
    dependencies=[Depends(current_user)],
    status_code=status.HTTP_204_NO_CONTENT,
    responses=responses.logout_user,
)
async def logout_user(res: Response) -> None:
    res.delete_cookie(key=Cookie.REFRESH_TOKEN.value)

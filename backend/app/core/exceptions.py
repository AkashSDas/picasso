from typing import Any

from fastapi import status


class NonUpdateableColumnError(AttributeError):
    """
    This is an exception that is raised when a non-updateable column is
    attempted to be updated.
    """

    def __init__(
        self,
        cls: str,
        column: str,
        old_value: str,
        new_value: str,
        message: str | None = None,
    ) -> None:
        self.cls = cls
        self.column = column
        self.old_value = old_value
        self.new_value = new_value

        if message is None:
            self.message = (
                f"Cannot update column {column} on model {cls} from "
                f"{old_value} to {new_value}: column is non-updateable"
            )


# ============================
# Http Errors
# ============================


class HttpError(Exception):
    def __init__(
        self,
        status_code: int,
        message: str,
        reason: str,
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        self.status_code = status_code
        self.message = message
        self.reason = reason
        self.context = context
        self.headers = headers


class BadRequestError(HttpError):
    def __init__(
        self,
        message: str = "Bad Request",
        reason: str = "Bad Request",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )


class ConflictError(HttpError):
    def __init__(
        self,
        message: str = "Conflict",
        reason: str = "Conflict",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )


class ForbiddenError(HttpError):
    def __init__(
        self,
        message: str = "Forbidden",
        reason: str = "Forbidden",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )


class InternalServerError(HttpError):
    def __init__(
        self,
        message: str = "Internal Server Error",
        reason: str = "Internal Server Error",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )


class NotFoundError(HttpError):
    def __init__(
        self,
        message: str = "Not Found",
        reason: str = "Not Found",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )


class UnauthorizedError(HttpError):
    def __init__(
        self,
        message: str = "Unauthorized",
        reason: str = "Unauthorized",
        context: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message=message,
            reason=reason,
            context=context,
            headers=headers,
        )

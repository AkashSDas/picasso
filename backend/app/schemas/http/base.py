from typing import Any

from pydantic import BaseModel, RootModel

# ===========================
# Utilities
# ===========================


class ErrorResponse(BaseModel):
    reason: str
    message: str


class PydanticErrorResponse(ErrorResponse):
    errors: list[Any]


# ===========================
# Http Error Responses
# ===========================


class BadRequestErrorResponse(RootModel[PydanticErrorResponse | ErrorResponse]):
    pass


class ConflictErrorResponse(ErrorResponse):
    pass


class EntityTooLargeErrorResponse(ErrorResponse):
    pass


class ForbiddenErrorResponse(ErrorResponse):
    pass


class InternalServerErrorResponse(ErrorResponse):
    pass


class NotFoundErrorResponse(ErrorResponse):
    pass


class UnauthorizedErrorResponse(ErrorResponse):
    pass


class UnsupportedMediaTypeErrorResponse(ErrorResponse):
    pass

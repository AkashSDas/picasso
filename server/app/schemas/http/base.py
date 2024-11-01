from typing import Any

from pydantic import BaseModel

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


class BadRequestErrorResponse(BaseModel):
    __root__: PydanticErrorResponse | ErrorResponse


class ConflictErrorResponse(ErrorResponse):
    pass


class InternalServerErrorResponse(ErrorResponse):
    pass


class NotFoundErrorResponse(ErrorResponse):
    pass


class UnauthorizedErrorResponse(ErrorResponse):
    pass

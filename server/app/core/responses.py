from typing import Any

from fastapi import status

from app import schemas

Responses = dict[int | str, dict[str, Any]]

# =======================
# Base
# =======================

_base_responses: Responses = {
    status.HTTP_500_INTERNAL_SERVER_ERROR: {
        "description": "Internal Server Error",
        "model": schemas.http.InternalServerErrorResponse,
    },
}

_bad_request_response: Responses = {
    status.HTTP_400_BAD_REQUEST: {
        "description": "Bad Request",
        "model": schemas.http.BadRequestErrorResponse,
    },
}

_not_found_response: Responses = {
    status.HTTP_404_NOT_FOUND: {
        "description": "Not Found",
        "model": schemas.http.NotFoundErrorResponse,
    }
}

_unauthorized_response: Responses = {
    status.HTTP_401_UNAUTHORIZED: {
        "description": "Unauthorized",
        "model": schemas.http.UnauthorizedErrorResponse,
    }
}

_forbidden_response: Responses = {
    status.HTTP_403_FORBIDDEN: {
        "description": "Forbidden",
        "model": schemas.http.ForbiddenErrorResponse,
    }
}


# =======================
# Auth
# =======================


email_signup: Responses = {
    status.HTTP_201_CREATED: {
        "description": "User account created and magic link login sent to email",
        "model": schemas.http.EmailSignupOut,
    },
    status.HTTP_409_CONFLICT: {
        "description": "Username or email already taken",
        "model": schemas.http.ConflictErrorResponse,
    },
    **_base_responses,
    **_bad_request_response,
}

email_login: Responses = {
    status.HTTP_200_OK: {
        "description": "Magic link login sent to email",
        "model": schemas.http.EmailLoginOut,
    },
    **_base_responses,
    **_bad_request_response,
}


complete_email_login: Responses = {
    status.HTTP_200_OK: {
        "description": "Magic link login sent to email",
        "model": schemas.http.CompleteEmailLoginOut,
    },
    **_base_responses,
    **_bad_request_response,
}


refresh_access_token: Responses = {
    status.HTTP_200_OK: {
        "description": "Refresh access token",
        "model": schemas.http.RefreshAccessTokenOut,
    },
    **_base_responses,
    **_bad_request_response,
    **_unauthorized_response,
}

logout_user: Responses = {
    status.HTTP_204_NO_CONTENT: {"description": "User logged out"},
    **_base_responses,
    **_unauthorized_response,
}


# =======================
# Style Filter
# =======================


upload_style_filters: Responses = {
    status.HTTP_201_CREATED: {
        "description": "Style filters uploaded",
        "model": schemas.http.UploadStyleFiltersOut,
    },
    **_base_responses,
    **_bad_request_response,
    **_unauthorized_response,
}


delete_style_filters: Responses = {
    status.HTTP_204_NO_CONTENT: {"description": "Style filters deleted"},
    **_base_responses,
    **_bad_request_response,
    **_forbidden_response,
    **_unauthorized_response,
}

report_style_filter: Responses = {
    status.HTTP_200_OK: {
        "description": "Style filter is reported and banned (if crossed a threshold)",
        "model": schemas.http.ReportStyleFilterOut,
    },
    **_base_responses,
    **_bad_request_response,
    **_unauthorized_response,
}


get_style_filters: Responses = {
    status.HTTP_200_OK: {
        "description": "Get style filters",
        "model": schemas.http.GetStyleFiltersOut,
    },
    **_base_responses,
    **_bad_request_response,
    **_unauthorized_response,
}

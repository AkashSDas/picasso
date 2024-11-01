import time

from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

from app.api import auth_router, example_router
from app.core import settings
from app.core.exceptions import BadRequestError
from app.utils.enums import HttpHeader

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    docs_url="/api/docs",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# Middlewares
# =========================

# This middleware will add unique request ID to each request for tracking
app.add_middleware(CorrelationIdMiddleware, header_name=HttpHeader.REQUEST_ID.value)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],
    allow_credentials=True,  # Allow credentials (cookies, etc.)
)

# Compresses response data for faster transmission and smaller payloads
app.add_middleware(GZipMiddleware, minimum_size=500)  # 500 bytes

if settings.environment == "production":
    # Automatically redirect HTTP requests to HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # Prevents host header attacks by validating allowed hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[str(host) for host in settings.trusted_hosts],
    )


# Custom middleware for adding security headers (optional)
@app.middleware("http")
async def add_security_headers(request, call_next):
    response = await call_next(request)

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Prevent Clickjacking
    response.headers["X-Frame-Options"] = "DENY"

    # Enable XSS protection in browsers
    response.headers["X-XSS-Protection"] = "1; mode=block"

    return response


@app.middleware("http")
async def add_process_time_header(req: Request, call_next) -> Response:
    start_time = time.time()
    response = await call_next(req)
    process_time = time.time() - start_time
    response.headers[HttpHeader.PROCESS_TIME.value] = str(process_time)
    return response


# =========================
# Error Handlers
# =========================


@app.exception_handler(BadRequestError)
async def bad_request_err_handler(_: Request, e: BadRequestError) -> JSONResponse:
    content = {"detail": e.detail}
    if e.context:
        content = {**content, **e.context}

    return JSONResponse(status_code=e.status_code, content=content)


@app.exception_handler(RequestValidationError)
async def validation_err_handler(_: Request, e: RequestValidationError) -> JSONResponse:
    content = {"detail": "Validation Error", "errors": e.errors()}
    return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content=content)


# =========================
# Routers
# =========================

app.include_router(example_router, prefix="/api/example", tags=["Example"])
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    res = RedirectResponse(url="/api/docs")
    return res

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

from app import schemas
from app.api import auth_router, example_router
from app.core import settings
from app.core.exceptions import BadRequestError

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    docs_url="/api/docs",
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# =========================
# Middlewares
# =========================

# Correlation ID Middleware: Adds unique request ID (X-Request-ID) to each
# request for tracking
app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")

# CORS Middleware: Allows cross-origin requests, useful for API integrations and
# frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_methods=["*"],
    allow_headers=["X-Request-ID"],  # Allowed request headers
    # Expose the headers you need
    expose_headers=["X-Request-ID", "X-Process-Time"],
)

# GZip Middleware: Compresses response data for faster transmission and smaller
# payloads. Compress responses larger than 500 bytes
app.add_middleware(GZipMiddleware, minimum_size=500)

if settings.environment == "production":
    # HTTPS Redirect Middleware: Automatically redirects HTTP requests to HTTPS
    app.add_middleware(HTTPSRedirectMiddleware)

    # Trusted Host Middleware: Prevents Host Header attacks by validating
    # allowed hosts
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=[str(host) for host in settings.trusted_hosts],
    )


# Custom Middleware for adding security headers (Optional, useful for
# additional security)
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
    response.headers["X-Process-Time"] = str(process_time)
    return response


# =========================
# Error Handlers
# =========================


@app.exception_handler(BadRequestError)
async def bad_request_err_handler(_: Request, e: BadRequestError) -> JSONResponse:
    content = {"detail": e.detail}
    if e.context:
        content = {**content, **e.context}

    return JSONResponse(
        status_code=e.status_code,
        content=schemas.SignupEmailAlreadyExistOut(**content).model_dump(by_alias=True),
    )


@app.exception_handler(RequestValidationError)
async def validation_err_handler(_: Request, e: RequestValidationError) -> JSONResponse:
    content = {"detail": "Validation error", "errors": e.errors()}
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

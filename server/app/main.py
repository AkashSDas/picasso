import time
from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware

from app.core.config import settings
from app.api import test_router

app = FastAPI(
    title=settings.app_title,
    version=settings.app_version,
    docs_url="/api/docs",  # Custom docs URL
)

# =========================
# Middlewares
# =========================

# Correlation ID Middleware: Adds unique request ID (X-Request-ID) to each request for tracking
app.add_middleware(CorrelationIdMiddleware, header_name="X-Request-ID")

# CORS Middleware: Allows cross-origin requests, useful for API integrations and frontend apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.cors_origins],  # Allowed origins
    allow_credentials=True,  # Allow credentials (cookies, etc.)
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, etc.)
    allow_headers=["X-Request-ID"],  # Allowed request headers
    expose_headers=["X-Request-ID"],  # Expose X-Request-ID for tracking purposes
)

# Trusted Host Middleware: Prevents Host Header attacks by validating allowed hosts
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=[str(host) for host in settings.trusted_hosts],
)

# GZip Middleware: Compresses response data for faster transmission and smaller payloads
# Compress responses larger than 500 bytes
app.add_middleware(GZipMiddleware, minimum_size=500)

# HTTPS Redirect Middleware: Automatically redirects HTTP requests to HTTPS (for production use)
app.add_middleware(HTTPSRedirectMiddleware)


# Custom Middleware for adding security headers (Optional, useful for additional security)
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
# Routers
# =========================

app.include_router(test_router, prefix="/api/test", tags=["test"])


@app.get("/", include_in_schema=False)
async def redirect_to_docs() -> RedirectResponse:
    res = RedirectResponse(url="/api/docs")
    return res
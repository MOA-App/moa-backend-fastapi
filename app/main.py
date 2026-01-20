from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.shared.presentation.middlewares.cors_middleware import setup_cors
from app.shared.presentation.middlewares.request_id_middleware import RequestIdMiddleware
from app.shared.presentation.middlewares.security_headers_middleware import SecurityHeadersMiddleware
from app.modules.auth.setup import setup_auth_module

# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# -----------------------------------------------------------------------------
# LIFESPAN
# -----------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting application...")
    logger.info(f"📝 Environment: {settings.ENVIRONMENT}")
    logger.info(
        f"🗄️  Database: "
        f"{settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}"
    )

    yield

    logger.info("🛑 Shutting down application...")


# -----------------------------------------------------------------------------
# APP
# -----------------------------------------------------------------------------

app = FastAPI(
    title=settings.APP_NAME,
    description="API de Autenticação com Clean Architecture",
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)


# -----------------------------------------------------------------------------
# GLOBAL MIDDLEWARES
# -----------------------------------------------------------------------------

setup_cors(app)
app.add_middleware(RequestIdMiddleware)
app.add_middleware(SecurityHeadersMiddleware)


# -----------------------------------------------------------------------------
# MODULES
# -----------------------------------------------------------------------------

setup_auth_module(app)

# setup_users_module(app)
# setup_products_module(app)


# -----------------------------------------------------------------------------
# ROOT ENDPOINTS
# -----------------------------------------------------------------------------

@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "Disabled",
        "health": "/health",
    }


@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
    }


# -----------------------------------------------------------------------------
# GLOBAL EXCEPTION HANDLERS
# -----------------------------------------------------------------------------

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail,
            "path": request.url.path,
        },
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    logger.error("Unhandled exception", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
        },
    )


# -----------------------------------------------------------------------------
# ENTRYPOINT (DEV)
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info",
    )

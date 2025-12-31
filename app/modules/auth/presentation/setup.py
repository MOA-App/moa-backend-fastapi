from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from .routes.auth_routes import router as auth_router
from .routes.auth_routes import role_router, permission_router, user_router
from .middlewares.auth_middleware import AuthLoggingMiddleware, RateLimitMiddleware
from .exception_handlers import (
    auth_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from ...domain.exceptions.auth_exceptions import AuthException


def setup_auth_module(app: FastAPI) -> None:
    """
    Configura o módulo de autenticação na aplicação.
    
    - Registra routers
    - Adiciona middlewares
    - Registra exception handlers
    """
    
    # Registrar routers
    app.include_router(auth_router)
    app.include_router(role_router)
    app.include_router(permission_router)
    app.include_router(user_router)
    
    # Adicionar middlewares
    app.add_middleware(AuthLoggingMiddleware)
    app.add_middleware(RateLimitMiddleware, max_requests=5, window_seconds=60)
    
    # Registrar exception handlers
    app.add_exception_handler(AuthException, auth_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

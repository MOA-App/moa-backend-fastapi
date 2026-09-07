from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.modules.auth.domain.exceptions.auth_exceptions import AuthException
from app.modules.auth.presentation.middlewares.exception_handler import (
    domain_exception_handler,
    validation_exception_handler,
)
from app.modules.auth.presentation.routes import permission_routes
from app.modules.auth.presentation.routes import role_routes
from app.modules.auth.presentation.routes import user_routes
from app.modules.auth.presentation.routes import auth_routes


def setup_auth_module(app: FastAPI) -> None:
    """
    Configura o módulo de autenticação na aplicação.
    
    - Registra routers
    - Adiciona middlewares
    - Registra exception handlers
    """
    
    # Registrar routers
    app.include_router(auth_routes.router)

    app.include_router(permission_routes.router)

    app.include_router(role_routes.router)

    app.include_router(user_routes.router)

    # Registrar exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(AuthException, domain_exception_handler)

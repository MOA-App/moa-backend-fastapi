from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.modules.auth.presentation.middlewares.exception_handler import validation_exception_handler
from app.modules.auth.presentation.routes import permission_routes



def setup_auth_module(app: FastAPI) -> None:
    """
    Configura o módulo de autenticação na aplicação.
    
    - Registra routers
    - Adiciona middlewares
    - Registra exception handlers
    """
    
    # Registrar routers
    app.include_router(permission_routes.router)

    # Registrar exception handlers
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

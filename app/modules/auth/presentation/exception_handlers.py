from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from ...domain.exceptions.auth_exceptions import (
    AuthException,
    UserAlreadyExistsException,
    InvalidCredentialsException,
    UserNotFoundException,
    UnauthorizedException,
    InsufficientPermissionsException,
    DomainValidationException,
    RepositoryException
)


async def auth_exception_handler(request: Request, exc: AuthException) -> JSONResponse:
    """
    Handler global para exceções de autenticação do domínio.
    """
    
    # Mapear exceções para status codes
    status_map = {
        UserAlreadyExistsException: status.HTTP_400_BAD_REQUEST,
        InvalidCredentialsException: status.HTTP_401_UNAUTHORIZED,
        UserNotFoundException: status.HTTP_404_NOT_FOUND,
        UnauthorizedException: status.HTTP_403_FORBIDDEN,
        InsufficientPermissionsException: status.HTTP_403_FORBIDDEN,
        DomainValidationException: status.HTTP_400_BAD_REQUEST,
        RepositoryException: status.HTTP_500_INTERNAL_SERVER_ERROR,
    }
    
    status_code = status_map.get(type(exc), status.HTTP_400_BAD_REQUEST)
    
    return JSONResponse(
        status_code=status_code,
        content={
            "error": exc.__class__.__name__,
            "message": str(exc)
        }
    )


async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """
    Handler para erros de validação do Pydantic.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "message": "Dados inválidos fornecidos",
            "details": errors
        }
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Handler genérico para exceções não tratadas.
    """
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "internal_server_error",
            "message": "Erro interno do servidor"
        }
    )

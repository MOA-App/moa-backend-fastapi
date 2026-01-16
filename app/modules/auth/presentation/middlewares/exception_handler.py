from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from typing import Union
import logging

from app.domain.exceptions.permission_exceptions import (
    PermissionNotFoundException,
    PermissionAlreadyExistsException,
    InvalidPermissionNameException,
)
from app.shared.domain.exceptions.repository_exception import RepositoryException
from ..exceptions import (
    BaseHTTPException,
    NotFoundException,
    ConflictException,
    BadRequestException,
    InternalServerException,
)

logger = logging.getLogger(__name__)


async def http_exception_handler(
    request: Request, 
    exc: BaseHTTPException
) -> JSONResponse:
    """Handler para exceções HTTP customizadas"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail.get("message"),
            "errors": exc.detail.get("errors", []),
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


async def validation_exception_handler(
    request: Request, 
    exc: Union[RequestValidationError, ValidationError]
) -> JSONResponse:
    """Handler para erros de validação do Pydantic"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "success": False,
            "message": "Erro de validação",
            "errors": errors,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )


async def domain_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handler para exceções de domínio"""
    
    # Mapeia exceções de domínio para HTTP
    if isinstance(exc, PermissionNotFoundException):
        http_exc = NotFoundException(str(exc))
        return await http_exception_handler(request, http_exc)
    
    elif isinstance(exc, PermissionAlreadyExistsException):
        http_exc = ConflictException(str(exc))
        return await http_exception_handler(request, http_exc)
    
    elif isinstance(exc, InvalidPermissionNameException):
        http_exc = BadRequestException(str(exc))
        return await http_exception_handler(request, http_exc)
    
    elif isinstance(exc, RepositoryException):
        logger.error(f"Repository error: {exc}", exc_info=True)
        http_exc = InternalServerException(
            "Erro ao acessar dados. Tente novamente mais tarde."
        )
        return await http_exception_handler(request, http_exc)
    
    # Erro genérico não tratado
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "success": False,
            "message": "Erro interno do servidor",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    )

import datetime
import logging
from typing import Union

from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError

from app.modules.auth.domain.exceptions.auth_exceptions import (
    DomainValidationException,
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
    RepositoryException,
)

logger = logging.getLogger(__name__)


def _base_error_response(
    *,
    status_code: int,
    message: str,
    errors: list | None = None,
) -> JSONResponse:
    """Formato padrão de erro da API"""
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "errors": errors or [],
            "timestamp": datetime.datetime.now(
                datetime.timezone.utc
            ).isoformat(),
        },
    )


# ============================================================================
# VALIDATION ERRORS (FastAPI / Pydantic)
# ============================================================================

async def validation_exception_handler(
    _request: Request,
    exc: Union[RequestValidationError, ValidationError],
) -> JSONResponse:
    errors = [
        {
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"],
        }
        for error in exc.errors()
    ]

    return _base_error_response(
        status_code=status.HTTP_400_BAD_REQUEST,
        message="Erro de validação",
        errors=errors,
    )


# ============================================================================
# DOMAIN ERRORS → HTTP
# ============================================================================

async def domain_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:
    """
    Converte exceções de domínio em respostas HTTP.
    As routes NÃO tratam exceções.
    """

    # -------- NOT FOUND (404)
    if isinstance(exc, PermissionNotFoundException):
        return _base_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=str(exc),
        )

    # -------- CONFLICT (409)
    if isinstance(exc, PermissionAlreadyExistsException):
        return _base_error_response(
            status_code=status.HTTP_409_CONFLICT,
            message=str(exc),
        )

    # -------- BAD REQUEST (400)
    if isinstance(exc, DomainValidationException):
        return _base_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
        )

    # -------- INTERNAL ERROR (500 - repository)
    if isinstance(exc, RepositoryException):
        logger.error(
            f"Repository error: {exc}",
            exc_info=True,
        )
        return _base_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Erro ao acessar dados. Tente novamente mais tarde.",
        )

    # -------- FALLBACK (500)
    logger.error(
        f"Unhandled exception: {exc}",
        exc_info=True,
    )
    return _base_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Erro interno do servidor",
    )

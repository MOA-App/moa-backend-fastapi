import datetime
import logging
from typing import Union

from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.modules.auth.domain.exceptions.auth_exceptions import (
    DomainValidationException,

    # Permission
    PermissionAlreadyExistsException,
    PermissionNotFoundException,

    # Role
    RoleAlreadyExistsException,
    RoleAlreadyAssignedException,
    RoleNotAssignedException,
    RoleNotFoundException,

    # User
    UserAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyActiveException,
    UserAlreadyInactiveException,
)

from app.modules.auth.infrastructure.exceptions.repository_exception import (
    RepositoryException,
)

logger = logging.getLogger(__name__)


# ============================================================================
# BASE RESPONSE
# ============================================================================

def _base_error_response(
    *,
    status_code: int,
    message: str,
    errors: list | None = None,
) -> JSONResponse:
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
# VALIDATION ERRORS
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
# DOMAIN ERRORS
# ============================================================================

async def domain_exception_handler(
    _request: Request,
    exc: Exception,
) -> JSONResponse:

    # ------------------------------------------------------------------------
    # NOT FOUND
    # ------------------------------------------------------------------------

    if isinstance(
        exc,
        (
            PermissionNotFoundException,
            RoleNotFoundException,
            UserNotFoundException,
        ),
    ):
        return _base_error_response(
            status_code=status.HTTP_404_NOT_FOUND,
            message=str(exc),
        )

    # ------------------------------------------------------------------------
    # CONFLICT
    # ------------------------------------------------------------------------

    if isinstance(
        exc,
        (
            PermissionAlreadyExistsException,
            RoleAlreadyExistsException,
            RoleAlreadyAssignedException,
            UserAlreadyExistsException,
            UserAlreadyActiveException,
            UserAlreadyInactiveException,
        ),
    ):
        return _base_error_response(
            status_code=status.HTTP_409_CONFLICT,
            message=str(exc),
        )

    # ------------------------------------------------------------------------
    # BAD REQUEST
    # ------------------------------------------------------------------------

    if isinstance(
        exc,
        (
            DomainValidationException,
            RoleNotAssignedException,
        ),
    ):
        return _base_error_response(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=str(exc),
        )

    # ------------------------------------------------------------------------
    # REPOSITORY
    # ------------------------------------------------------------------------

    if isinstance(exc, RepositoryException):
        logger.exception(exc)

        return _base_error_response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message="Erro ao acessar os dados. Tente novamente mais tarde.",
        )

    # ------------------------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------------------------

    logger.exception(exc)

    return _base_error_response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        message="Erro interno do servidor",
    )



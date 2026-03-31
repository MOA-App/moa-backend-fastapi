from fastapi import Request
from fastapi.responses import JSONResponse

from app.modules.auth.domain.exceptions.auth_exceptions import (
    RoleNotFoundException,
    RoleAlreadyExistsException,
    RoleAlreadyAssignedException,
    RoleNotAssignedException,
)


def register_exception_handlers(app):

    @app.exception_handler(RoleNotFoundException)
    async def role_not_found_handler(request: Request, exc: RoleNotFoundException):
        return JSONResponse(
            status_code=404,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RoleAlreadyExistsException)
    async def role_exists_handler(request: Request, exc: RoleAlreadyExistsException):
        return JSONResponse(
            status_code=409,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RoleAlreadyAssignedException)
    async def role_assigned_handler(request: Request, exc: RoleAlreadyAssignedException):
        return JSONResponse(
            status_code=409,
            content={"success": False, "message": str(exc)},
        )

    @app.exception_handler(RoleNotAssignedException)
    async def role_not_assigned_handler(request: Request, exc: RoleNotAssignedException):
        return JSONResponse(
            status_code=400,
            content={"success": False, "message": str(exc)},
        )

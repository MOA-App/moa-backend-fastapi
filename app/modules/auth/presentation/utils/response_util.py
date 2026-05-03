from typing import Any, Optional
from datetime import datetime, timezone
from fastapi import Response, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class ResponseUtil:
    """Utilitário para padronizar respostas HTTP"""

    @staticmethod
    def success(
        data: Any,
        status_code: int = status.HTTP_200_OK,
        message: Optional[str] = None
    ) -> JSONResponse:

        content = {
            "success": True,
            "message": message,
            "data": data,
        }

        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(content),
        )

    @staticmethod
    def created(data: Any, message: str = "Recurso criado com sucesso") -> JSONResponse:
        return ResponseUtil.success(
            data=data,
            status_code=status.HTTP_201_CREATED,
            message=message
        )

    @staticmethod
    def no_content() -> Response:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    @staticmethod
    def error(
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors: Optional[list] = None
    ) -> JSONResponse:

        content = {
            "success": False,
            "message": message,
            "errors": errors or [],
            "timestamp": datetime.now(timezone.utc),
        }

        return JSONResponse(
            status_code=status_code,
            content=jsonable_encoder(content),
        )

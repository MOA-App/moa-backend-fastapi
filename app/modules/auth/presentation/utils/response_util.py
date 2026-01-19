from typing import Any, Optional
from datetime import datetime, timezone
from fastapi import Response, status
from fastapi.responses import JSONResponse


class ResponseUtil:
    """Utilitário para padronizar respostas HTTP"""
    
    @staticmethod
    def success(
        data: Any,
        status_code: int = status.HTTP_200_OK,
        message: Optional[str] = None
    ) -> JSONResponse:
        """Resposta de sucesso padrão"""
        content = {
            "success": True,
            "data": data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        if message:
            content["message"] = message
        
        return JSONResponse(
            status_code=status_code,
            content=content
        )
    
    @staticmethod
    def created(data: Any, message: str = "Recurso criado com sucesso") -> JSONResponse:
        """Resposta para recurso criado (201)"""
        return ResponseUtil.success(
            data=data,
            status_code=status.HTTP_201_CREATED,
            message=message
        )
    
    @staticmethod
    def no_content() -> Response:
        """Resposta sem conteúdo (204)"""
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    @staticmethod
    def error(
        message: str,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        errors: Optional[list] = None
    ) -> JSONResponse:
        """Resposta de erro padrão"""
        return JSONResponse(
            status_code=status_code,
            content={
                "success": False,
                "message": message,
                "errors": errors or [],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        )

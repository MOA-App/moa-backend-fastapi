from typing import Optional, Dict, Any, List
from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Classe base para exceções HTTP customizadas"""
    
    def __init__(
        self,
        status_code: int,
        message: str,
        errors: Optional[List[Dict[str, Any]]] = None,
        headers: Optional[Dict[str, str]] = None
    ):
        detail = {
            "message": message,
            "errors": errors or []
        }
        super().__init__(status_code=status_code, detail=detail, headers=headers)


class BadRequestException(BaseHTTPException):
    """Exceção para requisições inválidas (400)"""
    
    def __init__(
        self, 
        message: str = "Requisição inválida",
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message=message,
            errors=errors
        )


class NotFoundException(BaseHTTPException):
    """Exceção para recurso não encontrado (404)"""
    
    def __init__(self, message: str = "Recurso não encontrado"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            message=message
        )


class ConflictException(BaseHTTPException):
    """Exceção para conflito de recursos (409)"""
    
    def __init__(
        self, 
        message: str = "Conflito de recursos",
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            message=message,
            errors=errors
        )


class UnprocessableEntityException(BaseHTTPException):
    """Exceção para entidade não processável (422)"""
    
    def __init__(
        self, 
        message: str = "Entidade não processável",
        errors: Optional[List[Dict[str, Any]]] = None
    ):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            message=message,
            errors=errors or []
        )


class InternalServerException(BaseHTTPException):
    """Exceção para erro interno do servidor (500)"""
    
    def __init__(self, message: str = "Erro interno do servidor"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=message
        )


class ValidationException(BaseHTTPException):
    """Exceção para erros de validação"""
    
    def __init__(self, errors: List[Dict[str, Any]]):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Falha na validação",
            errors=errors
        )

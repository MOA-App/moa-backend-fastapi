from typing import List
from pydantic import BaseModel, Field
from .permission_response import PermissionResponse


class PermissionListMeta(BaseModel):
    """Metadados de paginação"""
    
    total: int = Field(..., description="Total de registros")
    page: int = Field(..., description="Página atual")
    limit: int = Field(..., description="Itens por página")
    total_pages: int = Field(..., description="Total de páginas")


class PermissionListResponse(BaseModel):
    """Schema de resposta para listagem de permissões"""
    
    data: List[PermissionResponse] = Field(..., description="Lista de permissões")
    meta: PermissionListMeta = Field(..., description="Metadados de paginação")

    class Config:
        json_schema_extra = {
            "example": {
                "data": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "nome": "users.create",
                        "descricao": "Criar usuários",
                        "resource": "users",
                        "action": "create",
                        "data_criacao": "2024-01-15T10:30:00Z"
                    }
                ],
                "meta": {
                    "total": 50,
                    "page": 1,
                    "limit": 10,
                    "total_pages": 5
                }
            }
        }

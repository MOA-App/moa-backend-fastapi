from typing import List
from pydantic import BaseModel, Field
from .permission_response import PermissionResponse


class PermissionByResourceResponse(BaseModel):
    """Schema de resposta para permissões por recurso"""
    
    resource: str = Field(..., description="Nome do recurso")
    permissions: List[PermissionResponse] = Field(
        ..., 
        description="Lista de permissões do recurso"
    )
    count: int = Field(..., description="Quantidade de permissões")

    class Config:
        json_schema_extra = {
            "example": {
                "resource": "users",
                "permissions": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "nome": "users.create",
                        "descricao": "Criar usuários",
                        "resource": "users",
                        "action": "create",
                        "data_criacao": "2024-01-15T10:30:00Z"
                    }
                ],
                "count": 4
            }
        }

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PermissionResponse(BaseModel):
    """Schema de resposta básica de permissão"""
    
    id: str = Field(..., description="ID único da permissão")
    nome: str = Field(..., description="Nome da permissão (resource.action)")
    descricao: Optional[str] = Field(None, description="Descrição da permissão")
    resource: str = Field(..., description="Recurso da permissão")
    action: str = Field(..., description="Ação da permissão")
    data_criacao: datetime = Field(..., description="Data de criação")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nome": "users.create",
                "descricao": "Permite criar novos usuários",
                "resource": "users",
                "action": "create",
                "data_criacao": "2024-01-15T10:30:00Z"
            }
        }

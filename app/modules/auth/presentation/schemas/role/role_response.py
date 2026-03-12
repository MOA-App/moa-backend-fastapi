from typing import Optional, List
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import datetime


class PermissionSummaryResponse(BaseModel):
    """Schema resumido de permissão dentro da resposta de role."""

    id: UUID = Field(..., description="ID único da permissão")
    nome: str = Field(..., description="Nome da permissão (ex: users.create)")
    descricao: Optional[str] = Field(None, description="Descrição da permissão")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "nome": "users.create",
                "descricao": "Criar usuários",
            }
        }


class RoleResponse(BaseModel):
    """Schema de resposta completo de uma role."""

    id: UUID = Field(..., description="ID único da role")
    nome: str = Field(..., description="Nome da role (ex: admin)")
    permissions: List[PermissionSummaryResponse] = Field(
        default_factory=list,
        description="Permissões associadas à role",
    )
    data_criacao: Optional[datetime] = Field(
        None, description="Data de criação da role"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440001",
                "nome": "admin",
                "permissions": [
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440000",
                        "nome": "users.create",
                        "descricao": "Criar usuários",
                    }
                ],
                "data_criacao": "2024-01-15T10:30:00Z",
            }
        }

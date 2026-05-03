from typing import List
from pydantic import BaseModel, ConfigDict, Field
from .role_response import RoleResponse


class RoleListResponse(BaseModel):
    """Schema de resposta para listagem de roles."""

    roles: List[RoleResponse] = Field(..., description="Lista de roles")
    total: int = Field(..., description="Quantidade total de roles")

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "roles": [
                    {
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
                    },
                    {
                        "id": "550e8400-e29b-41d4-a716-446655440002",
                        "nome": "viewer",
                        "permissions": [],
                        "data_criacao": "2024-01-15T11:00:00Z",
                    },
                ],
                "total": 2,
            }
        }
    )

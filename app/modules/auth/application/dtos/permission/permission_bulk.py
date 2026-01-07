from pydantic import BaseModel, Field
from typing import List

from app.modules.auth.application.dtos.permission.permission_inputs import CreatePermissionDTO



class BulkCreatePermissionsDTO(BaseModel):
    """DTO para criar múltiplas permissões de uma vez"""
    permissions: List[CreatePermissionDTO] = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Lista de permissões a criar"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "permissions": [
                    {"nome": "users.create", "descricao": "Criar usuários"},
                    {"nome": "users.read", "descricao": "Visualizar usuários"},
                    {"nome": "users.update", "descricao": "Atualizar usuários"},
                    {"nome": "users.delete", "descricao": "Deletar usuários"}
                ]
            }
        }

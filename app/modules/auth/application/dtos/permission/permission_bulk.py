from pydantic import BaseModel, Field
from typing import List

from app.modules.auth.application.dtos.permission.permission_inputs import CreatePermissionDTO
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO

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

class BulkCreatePermissionsResponseDTO(BaseModel):
    """DTO de resposta para criação em lote"""
    created: List[PermissionResponseDTO] = Field(
        description="Permissões criadas com sucesso"
    )
    skipped: List[str] = Field(
        default_factory=list,
        description="Permissões que já existiam (ignoradas)"
    )
    errors: List[dict] = Field(
        default_factory=list,
        description="Erros durante a criação"
    )
    total_created: int
    total_skipped: int
    total_errors: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "created": [
                    {"id": "uuid", "nome": "users.create", "descricao": "Criar"}
                ],
                "skipped": ["users.read"],
                "errors": [
                    {"nome": "invalid.format", "error": "Formato inválido"}
                ],
                "total_created": 3,
                "total_skipped": 1,
                "total_errors": 1
            }
        }

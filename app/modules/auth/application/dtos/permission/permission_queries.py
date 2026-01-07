from pydantic import BaseModel, Field
from typing import Optional, List

from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO

class ListPermissionsQueryDTO(BaseModel):
    """DTO para query de listagem de permissões"""
    resource: Optional[str] = Field(
        None,
        description="Filtrar por recurso específico",
        examples=["users", "posts"]
    )
    search: Optional[str] = Field(
        None,
        min_length=1,
        max_length=100,
        description="Buscar por nome ou descrição"
    )
    page: int = Field(
        default=1,
        ge=1,
        description="Número da página"
    )
    page_size: int = Field(
        default=20,
        ge=1,
        le=100,
        description="Itens por página"
    )

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

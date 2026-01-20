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


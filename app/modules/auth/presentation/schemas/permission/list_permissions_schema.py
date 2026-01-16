from typing import Optional, Literal
from pydantic import BaseModel, Field


class ListPermissionsQuery(BaseModel):
    """Schema para filtros de listagem de permissões"""
    
    page: int = Field(
        default=1,
        ge=1,
        description="Número da página"
    )
    limit: int = Field(
        default=10,
        ge=1,
        le=100,
        description="Quantidade de itens por página"
    )
    search: Optional[str] = Field(
        default=None,
        max_length=100,
        description="Busca por nome ou descrição"
    )
    resource: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Filtrar por recurso específico (ex: users, posts)"
    )
    action: Optional[str] = Field(
        default=None,
        max_length=50,
        description="Filtrar por ação específica (ex: create, read)"
    )
    sort_by: Literal["nome", "data_criacao"] = Field(
        default="data_criacao",
        description="Campo para ordenação"
    )
    sort_order: Literal["asc", "desc"] = Field(
        default="desc",
        description="Ordem de ordenação"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "page": 1,
                "limit": 20,
                "resource": "users",
                "sort_by": "nome",
                "sort_order": "asc"
            }
        }

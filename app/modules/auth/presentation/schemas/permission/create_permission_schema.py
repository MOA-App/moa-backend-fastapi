from typing import Optional
from pydantic import BaseModel, Field, field_validator


class CreatePermissionRequest(BaseModel):
    """Schema para criação de permissão"""
    
    nome: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome da permissão no formato resource.action",
        examples=["users.create", "posts.delete", "roles.update"]
    )
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Descrição detalhada da permissão"
    )

    @field_validator("nome")
    @classmethod
    def normalize_nome(cls, v: str) -> str:
        return v.strip().lower()

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "users.create",
                "descricao": "Permite criar novos usuários no sistema"
            }
        }

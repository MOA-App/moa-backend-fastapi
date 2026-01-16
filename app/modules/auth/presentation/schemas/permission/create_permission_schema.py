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
    
    @field_validator('nome')
    @classmethod
    def validate_nome_format(cls, v: str) -> str:
        """Valida formato resource.action"""
        v = v.strip().lower()
        
        if '.' not in v:
            raise ValueError(
                "Nome deve estar no formato 'resource.action' (ex: users.create)"
            )
        
        parts = v.split('.')
        if len(parts) != 2:
            raise ValueError(
                "Nome deve conter exatamente um ponto separando resource e action"
            )
        
        resource, action = parts
        
        if not resource or not action:
            raise ValueError(
                "Resource e action não podem ser vazios"
            )
        
        # Valida caracteres permitidos
        if not resource.replace('_', '').isalnum():
            raise ValueError(
                "Resource deve conter apenas letras, números e underscores"
            )
        
        if not action.replace('_', '').isalnum():
            raise ValueError(
                "Action deve conter apenas letras, números e underscores"
            )
        
        return v
    
    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v: Optional[str]) -> Optional[str]:
        """Valida e normaliza descrição"""
        if v is not None:
            v = v.strip()
            return v if v else None
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "users.create",
                "descricao": "Permite criar novos usuários no sistema"
            }
        }

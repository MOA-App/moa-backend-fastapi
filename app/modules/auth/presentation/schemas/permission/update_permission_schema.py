from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator


class UpdatePermissionRequest(BaseModel):
    """Schema para atualização de permissão"""
    
    nome: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Novo nome da permissão no formato resource.action"
    )
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Nova descrição da permissão"
    )
    
    @field_validator('nome')
    @classmethod
    def validate_nome_format(cls, v: Optional[str]) -> Optional[str]:
        """Valida formato resource.action se fornecido"""
        if v is None:
            return v
            
        v = v.strip().lower()
        
        if '.' not in v:
            raise ValueError(
                "Nome deve estar no formato 'resource.action'"
            )
        
        parts = v.split('.')
        if len(parts) != 2:
            raise ValueError(
                "Nome deve conter exatamente um ponto"
            )
        
        resource, action = parts
        if not resource or not action:
            raise ValueError(
                "Resource e action não podem ser vazios"
            )
        
        return v
    
    @model_validator(mode='after')
    def validate_at_least_one_field(self):
        """Valida que ao menos um campo foi fornecido"""
        if self.nome is None and self.descricao is None:
            raise ValueError(
                "Ao menos um campo (nome ou descricao) deve ser fornecido"
            )
        return self

    class Config:
        json_schema_extra = {
            "example": {
                "descricao": "Nova descrição atualizada para a permissão"
            }
        }

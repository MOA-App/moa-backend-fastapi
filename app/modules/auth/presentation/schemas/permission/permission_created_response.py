from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class PermissionCreatedResponse(BaseModel):
    """Schema de resposta após criação de permissão"""
    
    id: str = Field(..., description="ID da permissão criada")
    nome: str = Field(..., description="Nome da permissão")
    descricao: Optional[str] = Field(None, description="Descrição")
    data_criacao: datetime = Field(..., description="Data de criação")
    message: str = Field(
        default="Permissão criada com sucesso",
        description="Mensagem de confirmação"
    )

    class Config:
        from_attributes = True

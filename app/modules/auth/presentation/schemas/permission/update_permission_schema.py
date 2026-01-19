from typing import Optional
from pydantic import BaseModel, Field


class UpdatePermissionRequest(BaseModel):
    """Schema para atualização de permissão"""
    
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Nova descrição da permissão"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "descricao": "Nova descrição atualizada para a permissão"
            }
        }

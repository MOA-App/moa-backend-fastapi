from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UpdatePermissionRequest(BaseModel):
    """Schema para atualização de permissão"""
    
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Nova descrição da permissão"
    )
    
    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "descricao": "Nova descrição atualizada para a permissão"
            }
        }
    )

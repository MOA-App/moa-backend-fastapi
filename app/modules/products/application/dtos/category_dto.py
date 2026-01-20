from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class CategoryCreateDTO(BaseModel):
    """DTO para criação de categoria"""
    name: str = Field(min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=512)


class CategoryUpdateDTO(BaseModel):
    """DTO para atualização de categoria"""
    name: Optional[str] = Field(None, min_length=1, max_length=120)
    description: Optional[str] = Field(None, max_length=512)


class CategoryResponseDTO(BaseModel):
    """DTO de resposta de categoria"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: datetime
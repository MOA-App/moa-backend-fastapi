from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from datetime import datetime


class ProductResponseDTO(BaseModel):
    """DTO de resposta de produto"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    price: Decimal
    sku: str
    category_id: str
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


class ProductWithCategoryResponseDTO(BaseModel):
    """DTO de resposta de produto com dados da categoria"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: Optional[str] = None
    price: Decimal
    sku: str
    category_id: str
    category_name: Optional[str] = None
    stock_quantity: int
    is_active: bool
    created_at: datetime
    updated_at: datetime


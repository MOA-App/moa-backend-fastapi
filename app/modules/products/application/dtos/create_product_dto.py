from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal


class CreateProductDTO(BaseModel):
    """DTO para criação de produto"""
    name: str = Field(..., min_length=1, max_length=255, description="Nome do produto")
    description: Optional[str] = Field(None, max_length=2000, description="Descrição do produto")
    price: Decimal = Field(..., gt=0, description="Preço do produto")
    sku: str = Field(..., min_length=1, max_length=50, description="Código SKU do produto")
    category_id: str = Field(..., description="ID da categoria do produto")
    stock_quantity: int = Field(default=0, ge=0, description="Quantidade em estoque")
    is_active: bool = Field(default=True, description="Se o produto está ativo")


class UpdateProductDTO(BaseModel):
    """DTO para atualização de produto"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, max_length=2000)
    price: Optional[Decimal] = Field(None, gt=0)
    sku: Optional[str] = Field(None, min_length=1, max_length=50)
    category_id: Optional[str] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


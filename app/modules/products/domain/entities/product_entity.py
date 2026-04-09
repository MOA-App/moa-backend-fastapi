from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal
import uuid


@dataclass
class ProductEntity:
    """Entidade de domínio para Produto"""
    id: str
    name: str
    price: Decimal
    sku: str
    category_id: str
    description: Optional[str] = None
    stock_quantity: int = 0
    is_active: bool = True
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()
        if not self.updated_at:
            self.updated_at = datetime.utcnow()

    def update_stock(self, quantity: int) -> None:
        """Atualiza a quantidade em estoque"""
        if quantity < 0:
            raise ValueError("Quantidade em estoque não pode ser negativa")
        self.stock_quantity = quantity
        self.updated_at = datetime.utcnow()

    def activate(self) -> None:
        """Ativa o produto"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Desativa o produto"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def is_in_stock(self) -> bool:
        """Verifica se o produto está em estoque"""
        return self.stock_quantity > 0 and self.is_active


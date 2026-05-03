from sqlalchemy import Column, String, Text, Numeric, Integer, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid

from app.shared.infrastructure.database.base import Base, TimestampMixin


class ProductModel(Base, TimestampMixin):
    """Modelo SQLAlchemy para Produto"""
    __tablename__ = "products"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Identificador único do produto"
    )
    name = Column(
        String(255),
        nullable=False,
        index=True,
        comment="Nome do produto"
    )
    description = Column(
        Text,
        nullable=True,
        comment="Descrição do produto"
    )
    price = Column(
        Numeric(10, 2),
        nullable=False,
        comment="Preço do produto"
    )
    sku = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
        comment="Código SKU do produto"
    )
    category_id = Column(
        UUID(as_uuid=True),
        ForeignKey("categories.id", ondelete="RESTRICT"),
        nullable=False,
        index=True,
        comment="ID da categoria do produto"
    )
    stock_quantity = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Quantidade em estoque"
    )
    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Se o produto está ativo"
    )

    # Relacionamento com categoria
    category = relationship("CategoryModel", backref="products")

    def __repr__(self):
        return f"<ProductModel(id={self.id}, name={self.name}, sku={self.sku})>"


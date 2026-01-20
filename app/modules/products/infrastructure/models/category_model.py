from sqlalchemy import Column, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid

from app.shared.infrastructure.database.base import Base, TimestampMixin


class CategoryModel(Base, TimestampMixin):
    """Modelo SQLAlchemy para Categoria"""
    __tablename__ = "categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        comment="Identificador único da categoria"
    )
    name = Column(
        String(120),
        unique=True,
        nullable=False,
        index=True,
        comment="Nome da categoria"
    )
    description = Column(
        Text,
        nullable=True,
        comment="Descrição da categoria"
    )

    def __repr__(self):
        return f"<CategoryModel(id={self.id}, name={self.name})>"


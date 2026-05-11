from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, DateTime
from datetime import datetime, timezone


class Base(DeclarativeBase):
    pass


class TimestampMixin:
    """
    Mixin para timestamps automáticos.
    """
    created_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Data de criação do registro"
    )

    updated_at = Column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Data da última atualização"
    )

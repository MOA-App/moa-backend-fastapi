from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, DateTime
from datetime import datetime

Base = declarative_base()
class TimestampMixin:
    """
    Mixin para adicionar timestamps de criação e atualização.
    """
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Data de criação do registro"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
        comment="Data da última atualização"
    )

from sqlalchemy import (
    Column,
    String,
    DateTime,
    Table,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.shared.infrastructure.database.base import Base, TimestampMixin


# ============================================================================
# TABELA DE ASSOCIAÇÃO (Many-to-Many: Role <-> Permission)
# ============================================================================

role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    ),
)


# ============================================================================
# TABELA DE ASSOCIAÇÃO (Many-to-Many: User <-> Role)
# ============================================================================

user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id",
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "role_id",
        UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    ),
)


class RoleModel(Base, TimestampMixin):
    __tablename__ = "roles"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
    )

    nome = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
    )

    data_criacao = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # ------------------------------------------------------------------------
    # RELATIONSHIPS
    # ------------------------------------------------------------------------

    permissions = relationship(
        "PermissionModel",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
    )

    users = relationship(
        "UserModel",
        secondary=user_roles,
        back_populates="roles",
        lazy="selectin",
    )

    def __repr__(self):
        return f"<RoleModel(id={self.id}, nome='{self.nome}')>"

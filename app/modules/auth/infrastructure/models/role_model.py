from sqlalchemy import Column, String, DateTime, Table, ForeignKey
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
        comment="ID da role",
    ),
    Column(
        "permission_id",
        UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
        comment="ID da permissão",
    ),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Data de associação",
    ),
)


class RoleModel(Base, TimestampMixin):
    """
    Model SQLAlchemy para Role.

    Representa a tabela 'roles' no banco de dados.

    Attributes:
        id: UUID único da role
        nome: Nome da role (único, lowercase, ex: admin)
        data_criacao: Data de criação da role

    Relationships:
        permissions: Permissões associadas à role (Many-to-Many)
    """

    __tablename__ = "roles"
    __table_args__ = {
        "comment": "Tabela de roles do sistema RBAC",
        "schema": None,
    }

    # ========================================================================
    # COLUMNS
    # ========================================================================

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="ID único da role",
    )

    nome = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Nome da role (ex: admin, editor, viewer)",
    )

    data_criacao = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Data e hora de criação da role",
    )

    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================

    permissions = relationship(
        "PermissionModel",
        secondary=role_permissions,
        back_populates="roles",
        lazy="selectin",
        cascade="save-update",
    )

    # ========================================================================
    # METHODS
    # ========================================================================

    def __repr__(self) -> str:
        return (
            f"<RoleModel("
            f"id={self.id}, "
            f"nome='{self.nome}'"
            f")>"
        )

    def __str__(self) -> str:
        return f"Role: {self.nome}"

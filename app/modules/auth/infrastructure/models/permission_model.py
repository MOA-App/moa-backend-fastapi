from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid

from app.shared.infrastructure.database.base import Base, TimestampMixin


class PermissionModel(Base, TimestampMixin):
    """
    Model SQLAlchemy para Permission.
    
    Representa a tabela 'permissions' no banco de dados.
    
    Attributes:
        id: UUID único da permissão
        nome: Nome da permissão (formato: resource.action)
        descricao: Descrição opcional da permissão
        data_criacao: Data de criação da permissão
        
    Relationships:
        roles: Roles que possuem esta permissão (Many-to-Many)
    """
    __tablename__ = 'permissions'
    __table_args__ = (
        {
            'comment': 'Tabela de permissões do sistema RBAC',
            'schema': None  # ou 'auth' se quiser usar schema
        }
    )
    
    # ========================================================================
    # COLUMNS
    # ========================================================================
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        nullable=False,
        comment="ID único da permissão"
    )
    
    nome = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True,
        comment="Nome da permissão no formato resource.action (ex: users.create)"
    )
    
    descricao = Column(
        Text,
        nullable=True,
        comment="Descrição detalhada da permissão"
    )
    
    data_criacao = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
        comment="Data e hora de criação da permissão"
    )
    
    # ========================================================================
    # RELATIONSHIPS
    # ========================================================================
    
    # Many-to-Many com Role através de role_permissions
    roles = relationship(
        "RoleModel",
        secondary="role_permissions",
        back_populates="permissions",
        lazy="selectin",  # Evita N+1 queries
        cascade="all, delete"
    )
    
    # ========================================================================
    # METHODS
    # ========================================================================
    
    def __repr__(self) -> str:
        """Representação string para debugging"""
        return (
            f"<PermissionModel("
            f"id={self.id}, "
            f"nome='{self.nome}', "
            f"descricao='{self.descricao[:30] if self.descricao else None}...'"
            f")>"
        )
    
    def __str__(self) -> str:
        """Representação string amigável"""
        return f"Permission: {self.nome}"
    
    def to_dict(self) -> dict:
        """
        Converte model para dicionário.
        
        Útil para serialização e debugging.
        """
        return {
            "id": str(self.id),
            "nome": self.nome,
            "descricao": self.descricao,
            "data_criacao": self.data_criacao.isoformat() if self.data_criacao else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

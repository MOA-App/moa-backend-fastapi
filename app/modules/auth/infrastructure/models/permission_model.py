"""
SQLAlchemy Model para Permission.

Este arquivo pode estar junto com os outros models em user_model.py
ou separado. Aqui está separado para clareza.
"""
from sqlalchemy import Column, String, DateTime, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from datetime import datetime
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
        default=datetime.utcnow,
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


# ============================================================================
# INDICES ADICIONAIS (Opcional - para performance)
# ============================================================================

from sqlalchemy import Index

# Índice para busca por prefixo (recurso)
# Útil para queries: WHERE nome LIKE 'users.%'
Index(
    'idx_permission_nome_prefix',
    PermissionModel.nome,
    postgresql_ops={'nome': 'text_pattern_ops'}
)

# Índice para busca full-text na descrição (PostgreSQL)
# Index(
#     'idx_permission_descricao_fulltext',
#     PermissionModel.descricao,
#     postgresql_using='gin',
#     postgresql_ops={'descricao': 'gin_trgm_ops'}
# )


# ============================================================================
# VERIFICAÇÃO DE INTEGRIDADE (Opcional)
# ============================================================================

from sqlalchemy import event
from sqlalchemy.orm import Session
import re


@event.listens_for(PermissionModel, 'before_insert')
@event.listens_for(PermissionModel, 'before_update')
def validate_permission_name(mapper, connection, target: PermissionModel):
    """
    Event listener para validar nome da permissão antes de insert/update.
    
    Garante que o nome está no formato correto mesmo que bypass o VO.
    """
    if not target.nome:
        raise ValueError("Nome da permissão não pode ser vazio")
    
    # Normalizar para lowercase
    target.nome = target.nome.lower().strip()
    
    # Validar formato: resource.action
    pattern = r'^[a-z0-9_]+(\.[a-z0-9_]+)+$'
    if not re.match(pattern, target.nome):
        raise ValueError(
            f"Formato inválido: '{target.nome}'. "
            f"Use 'resource.action' (ex: users.create)"
        )
    
    # Validar comprimento
    if len(target.nome) > 100:
        raise ValueError("Nome da permissão muito longo (máximo 100 caracteres)")
    
    # Limpar descrição
    if target.descricao:
        target.descricao = target.descricao.strip()
        if not target.descricao:
            target.descricao = None


# ============================================================================
# NOTA: Tabela associativa role_permissions
# ============================================================================
# A tabela role_permissions já deve estar definida em user_model.py:
#
# role_permissions = Table(
#     'role_permissions',
#     Base.metadata,
#     Column(
#         'role_id',
#         UUID(as_uuid=True),
#         ForeignKey('roles.id', ondelete='CASCADE'),
#         primary_key=True
#     ),
#     Column(
#         'permission_id',
#         UUID(as_uuid=True),
#         ForeignKey('permissions.id', ondelete='CASCADE'),
#         primary_key=True
#     ),
#     Column(
#         'assigned_at',
#         DateTime,
#         default=datetime.utcnow,
#         nullable=False,
#         comment="Data de atribuição da permissão à role"
#     )
# )


# ============================================================================
# MIGRATION SCRIPT (Alembic)
# ============================================================================
"""
Exemplo de migration que seria gerada:

```python
def upgrade():
    # Criar tabela permissions
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column('nome', sa.String(length=100), nullable=False),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('nome'),
        comment='Tabela de permissões do sistema RBAC'
    )
    
    # Criar índices
    op.create_index('idx_permission_nome', 'permissions', ['nome'])
    op.create_index(
        'idx_permission_nome_prefix',
        'permissions',
        ['nome'],
        postgresql_ops={'nome': 'text_pattern_ops'}
    )


def downgrade():
    op.drop_index('idx_permission_nome_prefix', table_name='permissions')
    op.drop_index('idx_permission_nome', table_name='permissions')
    op.drop_table('permissions')
```
"""

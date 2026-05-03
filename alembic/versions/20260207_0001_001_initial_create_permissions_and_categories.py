"""Create permissions and categories tables

Revision ID: 001_initial
Revises:
Create Date: 2026-02-07

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create permissions table
    op.create_table(
        'permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('nome', sa.String(100), nullable=False, unique=True, index=True),
        sa.Column('descricao', sa.Text(), nullable=True),
        sa.Column('data_criacao', sa.DateTime(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    # Create categories table
    op.create_table(
        'categories',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True,
                  server_default=sa.text('gen_random_uuid()')),
        sa.Column('name', sa.String(120), nullable=False, unique=True, index=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    )

    # Insert sample data for permissions
    op.execute("""
        INSERT INTO permissions (nome, descricao) VALUES
        ('permissions.create', 'Permite criar permissões'),
        ('permissions.read', 'Permite visualizar permissões'),
        ('permissions.update', 'Permite atualizar permissões'),
        ('permissions.delete', 'Permite excluir permissões'),
        ('categories.create', 'Permite criar categorias'),
        ('categories.read', 'Permite visualizar categorias'),
        ('categories.update', 'Permite atualizar categorias'),
        ('categories.delete', 'Permite excluir categorias')
        ON CONFLICT (nome) DO NOTHING
    """)

    # Insert sample data for categories
    op.execute("""
        INSERT INTO categories (name, description) VALUES
        ('Eletrônicos', 'Produtos eletrônicos em geral'),
        ('Roupas', 'Vestuário masculino e feminino'),
        ('Alimentos', 'Produtos alimentícios'),
        ('Móveis', 'Móveis para casa e escritório'),
        ('Livros', 'Livros e materiais de leitura')
        ON CONFLICT (name) DO NOTHING
    """)


def downgrade() -> None:
    op.drop_table('categories')
    op.drop_table('permissions')


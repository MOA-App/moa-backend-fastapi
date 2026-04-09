"""
Script para testar a conexão com o banco de dados e criar tabelas.
"""
import asyncio
import sys
sys.path.insert(0, '/home/qiqi2k2/PycharmProjects/moa-backend-fastapi')

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def test_and_create():
    """Testa conexão e cria tabelas se necessário."""

    # URL direto para evitar problemas com .env
    database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/moa_db"

    print(f"Connecting to database...")

    try:
        engine = create_async_engine(database_url, echo=True)

        async with engine.begin() as conn:
            # Testar conexão
            result = await conn.execute(text("SELECT 1"))
            print(f"Connection OK: {result.scalar()}")

            # Criar tabela permissions
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS permissions (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    nome VARCHAR(100) UNIQUE NOT NULL,
                    descricao TEXT,
                    data_criacao TIMESTAMP WITH TIME ZONE DEFAULT NOW() NOT NULL,
                    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
                )
            """))
            print("Table 'permissions' created/verified")

            # Criar tabela categories
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(120) UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
                )
            """))
            print("Table 'categories' created/verified")

            # Criar índices
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_permissions_nome ON permissions(nome)
            """))
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name)
            """))
            print("Indexes created/verified")

            # Inserir dados de teste
            await conn.execute(text("""
                INSERT INTO permissions (nome, descricao)
                VALUES 
                    ('permissions.create', 'Permite criar permissões'),
                    ('permissions.read', 'Permite visualizar permissões'),
                    ('permissions.update', 'Permite atualizar permissões'),
                    ('permissions.delete', 'Permite excluir permissões'),
                    ('categories.create', 'Permite criar categorias'),
                    ('categories.read', 'Permite visualizar categorias'),
                    ('categories.update', 'Permite atualizar categorias'),
                    ('categories.delete', 'Permite excluir categorias')
                ON CONFLICT (nome) DO NOTHING
            """))
            print("Sample permissions inserted")

            await conn.execute(text("""
                INSERT INTO categories (name, description)
                VALUES 
                    ('Eletrônicos', 'Produtos eletrônicos em geral'),
                    ('Roupas', 'Vestuário masculino e feminino'),
                    ('Alimentos', 'Produtos alimentícios')
                ON CONFLICT (name) DO NOTHING
            """))
            print("Sample categories inserted")

            # Verificar dados
            result = await conn.execute(text("SELECT COUNT(*) FROM permissions"))
            print(f"Total permissions: {result.scalar()}")

            result = await conn.execute(text("SELECT COUNT(*) FROM categories"))
            print(f"Total categories: {result.scalar()}")

        await engine.dispose()
        print("\n✅ Database setup complete!")
        return True

    except Exception as e:
        print(f"\n❌ Error: {type(e).__name__}: {e}")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_and_create())
    sys.exit(0 if success else 1)


#!/usr/bin/env python3
"""
Script para executar migrações e testar as implementações.
Executa: python scripts/run_migrations.py
"""
import asyncio
import sys
import os

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def run_migrations():
    """Cria as tabelas e insere dados de teste."""

    # URL de conexão
    database_url = "postgresql+asyncpg://postgres:postgres@localhost:5432/moa_db"

    print("=" * 60)
    print("  MOA Backend - Database Migration")
    print("=" * 60)
    print()

    try:
        print("🔌 Conectando ao banco de dados...")
        engine = create_async_engine(database_url)

        async with engine.begin() as conn:
            # Testar conexão
            result = await conn.execute(text("SELECT 1"))
            print(f"✅ Conexão estabelecida: {result.scalar()}")
            print()

            # Criar tabela permissions
            print("📋 Criando tabela 'permissions'...")
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
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_permissions_nome ON permissions(nome)
            """))
            print("   ✅ Tabela 'permissions' criada/verificada")

            # Criar tabela categories
            print("📋 Criando tabela 'categories'...")
            await conn.execute(text("""
                CREATE TABLE IF NOT EXISTS categories (
                    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                    name VARCHAR(120) UNIQUE NOT NULL,
                    description TEXT,
                    created_at TIMESTAMP DEFAULT NOW() NOT NULL,
                    updated_at TIMESTAMP DEFAULT NOW() NOT NULL
                )
            """))
            await conn.execute(text("""
                CREATE INDEX IF NOT EXISTS idx_categories_name ON categories(name)
            """))
            print("   ✅ Tabela 'categories' criada/verificada")
            print()

            # Inserir dados de teste para permissions
            print("📝 Inserindo dados de teste em 'permissions'...")
            await conn.execute(text("""
                INSERT INTO permissions (nome, descricao) VALUES
                ('permissions.create', 'Permite criar permissões'),
                ('permissions.read', 'Permite visualizar permissões'),
                ('permissions.update', 'Permite atualizar permissões'),
                ('permissions.delete', 'Permite excluir permissões'),
                ('categories.create', 'Permite criar categorias'),
                ('categories.read', 'Permite visualizar categorias'),
                ('categories.update', 'Permite atualizar categorias'),
                ('categories.delete', 'Permite excluir categorias'),
                ('products.create', 'Permite criar produtos'),
                ('products.read', 'Permite visualizar produtos'),
                ('products.update', 'Permite atualizar produtos'),
                ('products.delete', 'Permite excluir produtos')
                ON CONFLICT (nome) DO NOTHING
            """))

            result = await conn.execute(text("SELECT COUNT(*) FROM permissions"))
            count = result.scalar()
            print(f"   ✅ Total de permissões: {count}")

            # Inserir dados de teste para categories
            print("📝 Inserindo dados de teste em 'categories'...")
            await conn.execute(text("""
                INSERT INTO categories (name, description) VALUES
                ('Eletrônicos', 'Produtos eletrônicos em geral'),
                ('Roupas', 'Vestuário masculino e feminino'),
                ('Alimentos', 'Produtos alimentícios'),
                ('Móveis', 'Móveis para casa e escritório'),
                ('Livros', 'Livros e materiais de leitura'),
                ('Esportes', 'Artigos esportivos'),
                ('Beleza', 'Produtos de beleza e cuidados pessoais')
                ON CONFLICT (name) DO NOTHING
            """))

            result = await conn.execute(text("SELECT COUNT(*) FROM categories"))
            count = result.scalar()
            print(f"   ✅ Total de categorias: {count}")
            print()

            # Listar dados inseridos
            print("=" * 60)
            print("  DADOS INSERIDOS")
            print("=" * 60)
            print()

            print("📋 PERMISSIONS:")
            result = await conn.execute(text(
                "SELECT id, nome, descricao FROM permissions ORDER BY nome"
            ))
            for row in result.fetchall():
                print(f"   - {row[1]}: {row[2]}")
            print()

            print("📋 CATEGORIES:")
            result = await conn.execute(text(
                "SELECT id, name, description FROM categories ORDER BY name"
            ))
            for row in result.fetchall():
                print(f"   - {row[1]}: {row[2]}")
            print()

        await engine.dispose()

        print("=" * 60)
        print("  ✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        print()
        print("Próximos passos:")
        print("  1. Inicie a aplicação: uvicorn app.main:app --reload")
        print("  2. Acesse a documentação: http://localhost:8000/docs")
        print("  3. Execute os testes: bash scripts/test_api.sh")
        print()

        return True

    except Exception as e:
        print(f"\n❌ Erro: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(run_migrations())
    sys.exit(0 if success else 1)


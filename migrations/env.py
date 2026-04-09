"""
    run_migrations_online()
else:
    run_migrations_offline()
if context.is_offline_mode():


    asyncio.run(run_async_migrations())
    """Run migrations in 'online' mode."""
def run_migrations_online() -> None:


    await connectable.dispose()

        await connection.run_sync(do_run_migrations)
    async with connectable.connect() as connection:

    )
        poolclass=pool.NullPool,
        prefix="sqlalchemy.",
        config.get_section(config.config_ini_section, {}),
    connectable = async_engine_from_config(
    """Run migrations in 'online' mode with async engine."""
async def run_async_migrations() -> None:


        context.run_migrations()
    with context.begin_transaction():

    context.configure(connection=connection, target_metadata=target_metadata)
def do_run_migrations(connection: Connection) -> None:


        context.run_migrations()
    with context.begin_transaction():

    )
        dialect_opts={"paramstyle": "named"},
        literal_binds=True,
        target_metadata=target_metadata,
        url=url,
    context.configure(
    url = config.get_main_option("sqlalchemy.url")
    """Run migrations in 'offline' mode."""
def run_migrations_offline() -> None:


target_metadata = Base.metadata
# Metadata for 'autogenerate'

    fileConfig(config.config_file_name)
if config.config_file_name is not None:
# Setup loggers

config = context.config
# Alembic Config object

from app.modules.products.infrastructure.models.category_model import CategoryModel
from app.modules.auth.infrastructure.models.permission_model import PermissionModel
from app.shared.infrastructure.database.base import Base
# Import models

from alembic import context

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.engine import Connection
from sqlalchemy import pool

from logging.config import fileConfig
import asyncio
"""
Alembic environment configuration for async SQLAlchemy.


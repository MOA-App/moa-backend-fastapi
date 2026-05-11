import asyncio
import logging
from sqlalchemy import text

from app.shared.infrastructure.database.session import DatabaseSession

logger = logging.getLogger(__name__)


async def init_db():
    """
    Apenas testa conexão com o banco.
    Migrações são feitas pelo Alembic.
    """
    engine = DatabaseSession.get_engine()

    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))

    logger.info("Database connection successful")


if __name__ == "__main__":
    asyncio.run(init_db())

import logging
from sqlalchemy import text
from app.shared.infrastructure.database.session import DatabaseSession

logger = logging.getLogger(__name__)


async def check_database_health() -> dict:
    """
    Verifica saúde da conexão com banco de dados.
    Usado para healthcheck da API.
    """
    try:
        engine = DatabaseSession.get_engine()

        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))

        return {
            "status": "healthy",
            "database": "connected"
        }

    except Exception as e:
        logger.error(f"Database health check failed: {e}")
        return {
            "status": "unhealthy",
            "database": "disconnected",
            "error": str(e)
        }

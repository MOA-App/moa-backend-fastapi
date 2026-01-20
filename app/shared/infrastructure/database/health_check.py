from fastapi import logger
from app.shared.infrastructure.database.session import DatabaseSession


async def check_database_health() -> dict:
    """
    Verifica saúde da conexão com banco de dados.
    
    Returns:
        dict: Status da conexão
    """
    try:
        engine = DatabaseSession.get_engine()
        
        async with engine.connect() as conn:
            await conn.execute("SELECT 1")
        
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

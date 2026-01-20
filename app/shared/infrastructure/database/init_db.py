import asyncio
import logging
from sqlalchemy import text

from app.shared.infrastructure.database.base import Base
from app.shared.infrastructure.database.session import DatabaseSession
from app.modules.auth.infrastructure.models.permission_model import PermissionModel
from app.modules.products.infrastructure.models.category_model import CategoryModel

# ------------------------------------------------------------------
# LOGGING (ESSENCIAL)
# ------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# TABLE CREATION
# ------------------------------------------------------------------

async def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    
    ATENÇÃO: Use apenas em desenvolvimento!
    Em produção, use Alembic para migrações.
    """
    engine = DatabaseSession.get_engine()

    logger.info("Creating database tables...")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Database tables created successfully")


async def drop_tables():
    """
    Deleta todas as tabelas do banco de dados.
    
    ATENÇÃO: Use apenas em desenvolvimento/testes!
    """
    engine = DatabaseSession.get_engine()
    
    logger.warning("Dropping all database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    logger.info("Database tables dropped")


async def init_db():
    """
    Inicializa o banco de dados.
    Pode ser usado em startup da aplicação.
    """
    try:
        engine = DatabaseSession.get_engine()
        
        # Testar conexão
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        
        logger.info("Database connection successful")
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


# ------------------------------------------------------------------
# ENTRYPOINT
# ------------------------------------------------------------------

if __name__ == "__main__":
    asyncio.run(create_tables())

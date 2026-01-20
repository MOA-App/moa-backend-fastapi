from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    AsyncEngine
)
from typing import AsyncGenerator
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class DatabaseSession:
    """
    Gerenciador de sessão do banco de dados.
    Singleton pattern para engine.
    """
    _engine: AsyncEngine | None = None
    _session_factory: async_sessionmaker[AsyncSession] | None = None
    
    @classmethod
    def get_engine(cls) -> AsyncEngine:
        """Retorna engine do SQLAlchemy (singleton)"""
        if cls._engine is None:
            logger.info(f"Creating database engine: {settings.DATABASE_URL.split('@')[1]}")
            
            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=settings.DB_ECHO,
                future=True,
                pool_pre_ping=True,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_recycle=3600,  # Reciclar conexões após 1 hora
            )
        
        return cls._engine
    
    @classmethod
    def get_session_factory(cls) -> async_sessionmaker[AsyncSession]:
        """Retorna factory de sessões"""
        if cls._session_factory is None:
            engine = cls.get_engine()
            
            cls._session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autocommit=False,
                autoflush=False,
            )
        
        return cls._session_factory
    
    @classmethod
    async def close(cls) -> None:
        """Fecha engine e limpa recursos"""
        if cls._engine is not None:
            logger.info("Closing database engine")
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency para obter sessão do banco de dados.
    
    Uso:
        @router.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # usar db aqui
            pass
    """
    session_factory = DatabaseSession.get_session_factory()
    
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

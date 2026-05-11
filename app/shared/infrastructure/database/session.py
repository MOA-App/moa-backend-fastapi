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
    _engine: AsyncEngine | None = None
    _session_factory: async_sessionmaker[AsyncSession] | None = None

    @classmethod
    def get_engine(cls) -> AsyncEngine:
        if cls._engine is None:
            logger.info("Creating database engine")

            cls._engine = create_async_engine(
                settings.DATABASE_URL,
                echo=settings.DB_ECHO,
                pool_pre_ping=True,
                pool_size=settings.DB_POOL_SIZE,
                max_overflow=settings.DB_MAX_OVERFLOW,
                pool_recycle=3600,
            )

        return cls._engine

    @classmethod
    def get_session_factory(cls) -> async_sessionmaker[AsyncSession]:
        if cls._session_factory is None:
            engine = cls.get_engine()

            cls._session_factory = async_sessionmaker(
                engine,
                class_=AsyncSession,
                expire_on_commit=False,
                autoflush=False,
            )

        return cls._session_factory

    @classmethod
    async def close(cls) -> None:
        if cls._engine is not None:
            logger.info("Closing database engine")
            await cls._engine.dispose()
            cls._engine = None
            cls._session_factory = None


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    session_factory = DatabaseSession.get_session_factory()

    async with session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise

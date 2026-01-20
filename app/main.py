from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from app.core.database import get_db, engine
from app.shared.infrastructure.database.base import Base
from app.modules.products.presentation.routes.category_routes import router as category_router

# Importar modelos para que o Base.metadata conheça as tabelas
from app.modules.products.infrastructure.models.category_model import CategoryModel  # noqa

app = FastAPI(
    title="MOA API",
    version="0.1.0",
)

# Registrar rotas
app.include_router(category_router, prefix="/api/v1")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/")
async def root():
    return {"status": "ok"}


@app.get("/health")
async def health(db: AsyncSession = Depends(get_db)):
    await db.execute(text("SELECT 1"))
    return {"health": "healthy", "database": "connected"}
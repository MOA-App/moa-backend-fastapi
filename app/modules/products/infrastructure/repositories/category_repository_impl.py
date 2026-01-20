from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from ..models.category_model import CategoryModel
from ...domain.entities.category_entity import CategoryEntity
from ...domain.repositories.category_repository import CategoryRepositoryInterface


class CategoryRepositoryImpl(CategoryRepositoryInterface):
    """Implementação do repositório de categorias usando SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: CategoryModel) -> CategoryEntity:
        """Converte modelo para entidade de domínio"""
        return CategoryEntity(
            id=str(model.id),
            name=model.name,
            description=model.description,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CategoryEntity) -> CategoryModel:
        """Converte entidade de domínio para modelo"""
        return CategoryModel(
            id=entity.id,
            name=entity.name,
            description=entity.description
        )

    async def create(self, entity: CategoryEntity) -> CategoryEntity:
        """Cria uma nova categoria no banco de dados"""
        model = self._to_model(entity)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """Busca categoria por ID"""
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Optional[CategoryEntity]:
        """Busca categoria por nome"""
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.name == name)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self) -> List[CategoryEntity]:
        """Lista todas as categorias"""
        result = await self.session.execute(
            select(CategoryModel).order_by(CategoryModel.name)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def delete(self, category_id: str) -> bool:
        """Exclui uma categoria pelo ID"""
        result = await self.session.execute(
            delete(CategoryModel).where(CategoryModel.id == category_id)
        )
        await self.session.commit()
        return result.rowcount > 0


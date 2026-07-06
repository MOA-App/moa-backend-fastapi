from typing import Optional, List

from sqlalchemy import delete, select
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.category_entity import CategoryEntity
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ..exceptions.category_infra_exceptions import (
    CategoryDatabaseConnectionException,
    CategoryIntegrityException,
    CategoryRepositoryException,
)
from ..mappers.category_mapper import CategoryMapper
from ..models.category_model import CategoryModel


class CategoryRepositoryImpl(CategoryRepositoryInterface):
    """Implementação do repositório de categorias usando SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: CategoryEntity) -> CategoryEntity:
        """Cria uma nova categoria no banco de dados."""
        model = CategoryMapper.to_model(entity)

        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

        except IntegrityError as e:
            await self.session.rollback()
            raise CategoryIntegrityException(
                details=str(e.orig) if e.orig else str(e)
            )

        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise CategoryDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CategoryRepositoryException(
                operation="criar",
                details=str(e),
            )

        return CategoryMapper.to_entity(model)

    async def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """Busca uma categoria pelo ID."""
        try:
            result = await self.session.execute(
                select(CategoryModel).where(CategoryModel.id == category_id)
            )
            model = result.scalar_one_or_none()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise CategoryRepositoryException(
                operation="buscar por ID",
                details=str(e),
            )

        return CategoryMapper.to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Optional[CategoryEntity]:
        """Busca uma categoria pelo nome."""
        try:
            result = await self.session.execute(
                select(CategoryModel).where(CategoryModel.name == name)
            )
            model = result.scalar_one_or_none()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise CategoryRepositoryException(
                operation="buscar por nome",
                details=str(e),
            )

        return CategoryMapper.to_entity(model) if model else None

    async def get_all(self) -> List[CategoryEntity]:
        """Lista todas as categorias."""
        try:
            result = await self.session.execute(
                select(CategoryModel).order_by(CategoryModel.name)
            )
            models = result.scalars().all()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise CategoryRepositoryException(
                operation="listar",
                details=str(e),
            )

        return [CategoryMapper.to_entity(model) for model in models]

    async def delete(self, category_id: str) -> bool:
        """Exclui uma categoria pelo ID."""
        try:
            result = await self.session.execute(
                delete(CategoryModel).where(CategoryModel.id == category_id)
            )
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()
            raise CategoryIntegrityException(
                details=str(e.orig) if e.orig else str(e)
            )

        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise CategoryDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CategoryRepositoryException(
                operation="excluir",
                details=str(e),
            )

        return result.rowcount > 0

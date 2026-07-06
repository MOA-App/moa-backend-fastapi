from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DBAPIError

from ..models.category_model import CategoryModel
from ...domain.entities.category_entity import CategoryEntity
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ..exceptions.category_infra_exceptions import (
    CategoryRepositoryException,
    CategoryDatabaseConnectionException,
    CategoryIntegrityException,
    CategoryMappingException,
)


class CategoryRepositoryImpl(CategoryRepositoryInterface):
    """Implementação do repositório de categorias usando SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: CategoryModel) -> CategoryEntity:
        """Converte modelo para entidade de domínio"""
        try:
            return CategoryEntity(
                id=str(model.id),
                name=model.name,
                description=model.description,
                created_at=model.created_at,
                updated_at=model.updated_at
            )
        except Exception as e:
            raise CategoryMappingException(details=str(e))

    def _to_model(self, entity: CategoryEntity) -> CategoryModel:
        """Converte entidade de domínio para modelo"""
        try:
            return CategoryModel(
                id=entity.id,
                name=entity.name,
                description=entity.description
            )
        except Exception as e:
            raise CategoryMappingException(details=str(e))

    async def create(self, entity: CategoryEntity) -> CategoryEntity:
        """Cria uma nova categoria no banco de dados"""
        model = self._to_model(entity)
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)
        except IntegrityError as e:
            await self.session.rollback()
            raise CategoryIntegrityException(details=str(e.orig) if e.orig else str(e))
        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise CategoryDatabaseConnectionException(details=str(e))
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CategoryRepositoryException(operation="criar", details=str(e))

        return self._to_entity(model)

    async def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """Busca categoria por ID"""
        try:
            result = await self.session.execute(
                select(CategoryModel).where(CategoryModel.id == category_id)
            )
            model = result.scalar_one_or_none()
        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))
        except SQLAlchemyError as e:
            raise CategoryRepositoryException(operation="buscar por ID", details=str(e))

        return self._to_entity(model) if model else None

    async def get_by_name(self, name: str) -> Optional[CategoryEntity]:
        """Busca categoria por nome"""
        try:
            result = await self.session.execute(
                select(CategoryModel).where(CategoryModel.name == name)
            )
            model = result.scalar_one_or_none()
        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))
        except SQLAlchemyError as e:
            raise CategoryRepositoryException(operation="buscar por nome", details=str(e))

        return self._to_entity(model) if model else None

    async def get_all(self) -> List[CategoryEntity]:
        """Lista todas as categorias"""
        try:
            result = await self.session.execute(
                select(CategoryModel).order_by(CategoryModel.name)
            )
            models = result.scalars().all()
        except (DBAPIError, ConnectionRefusedError) as e:
            raise CategoryDatabaseConnectionException(details=str(e))
        except SQLAlchemyError as e:
            raise CategoryRepositoryException(operation="listar", details=str(e))

        return [self._to_entity(model) for model in models]

    async def delete(self, category_id: str) -> bool:
        """Exclui uma categoria pelo ID"""
        try:
            result = await self.session.execute(
                delete(CategoryModel).where(CategoryModel.id == category_id)
            )
            await self.session.commit()
        except IntegrityError as e:
            await self.session.rollback()
            # Ex: categoria em uso por produtos (foreign key violation)
            raise CategoryIntegrityException(details=str(e.orig) if e.orig else str(e))
        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise CategoryDatabaseConnectionException(details=str(e))
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise CategoryRepositoryException(operation="excluir", details=str(e))

        return result.rowcount > 0

from typing import Optional, List

from sqlalchemy import delete, func, select
from sqlalchemy.exc import DBAPIError, IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from ...domain.entities.product_entity import ProductEntity
from ...domain.repositories.product_repository import ProductRepositoryInterface
from ..exceptions.product_infra_exceptions import (
    ProductRepositoryException,
    ProductDatabaseConnectionException,
    ProductIntegrityException,
)
from ..mappers.product_mapper import ProductMapper
from ..models.product_model import ProductModel


class ProductRepositoryImpl(ProductRepositoryInterface):
    """Implementação do repositório de produtos usando SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, entity: ProductEntity) -> ProductEntity:
        """Cria um novo produto no banco de dados."""
        model = ProductMapper.to_model(entity)

        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)

        except IntegrityError as e:
            await self.session.rollback()
            raise ProductIntegrityException(
                details=str(e.orig) if e.orig else str(e)
            )

        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProductRepositoryException(
                operation="criar",
                details=str(e),
            )

        return ProductMapper.to_entity(model)

    async def get_by_id(self, product_id: str) -> Optional[ProductEntity]:
        """Busca produto por ID."""
        try:
            result = await self.session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            model = result.scalar_one_or_none()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="buscar por ID",
                details=str(e),
            )

        return ProductMapper.to_entity(model) if model else None

    async def get_by_sku(self, sku: str) -> Optional[ProductEntity]:
        """Busca produto por SKU."""
        try:
            result = await self.session.execute(
                select(ProductModel).where(ProductModel.sku == sku)
            )
            model = result.scalar_one_or_none()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="buscar por SKU",
                details=str(e),
            )

        return ProductMapper.to_entity(model) if model else None

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 100,
    ) -> List[ProductEntity]:
        """Lista todos os produtos com paginação."""
        try:
            result = await self.session.execute(
                select(ProductModel)
                .order_by(ProductModel.name)
                .offset(skip)
                .limit(limit)
            )
            models = result.scalars().all()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="listar",
                details=str(e),
            )

        return [ProductMapper.to_entity(model) for model in models]

    async def get_by_category(self, category_id: str) -> List[ProductEntity]:
        """Lista produtos de uma categoria."""
        try:
            result = await self.session.execute(
                select(ProductModel)
                .where(ProductModel.category_id == category_id)
                .order_by(ProductModel.name)
            )
            models = result.scalars().all()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="listar por categoria",
                details=str(e),
            )

        return [ProductMapper.to_entity(model) for model in models]

    async def update(self, entity: ProductEntity) -> Optional[ProductEntity]:
        """Atualiza um produto."""
        try:
            result = await self.session.execute(
                select(ProductModel).where(ProductModel.id == entity.id)
            )
            model = result.scalar_one_or_none()

            if not model:
                return None

            model.name = entity.name
            model.description = entity.description
            model.price = entity.price
            model.sku = entity.sku
            model.category_id = entity.category_id
            model.stock_quantity = entity.stock_quantity
            model.is_active = entity.is_active

            await self.session.commit()
            await self.session.refresh(model)

        except IntegrityError as e:
            await self.session.rollback()
            raise ProductIntegrityException(
                details=str(e.orig) if e.orig else str(e)
            )

        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProductRepositoryException(
                operation="atualizar",
                details=str(e),
            )

        return ProductMapper.to_entity(model)

    async def delete(self, product_id: str) -> bool:
        """Exclui um produto pelo ID."""
        try:
            result = await self.session.execute(
                delete(ProductModel).where(ProductModel.id == product_id)
            )
            await self.session.commit()

        except IntegrityError as e:
            await self.session.rollback()
            raise ProductIntegrityException(
                details=str(e.orig) if e.orig else str(e)
            )

        except (DBAPIError, ConnectionRefusedError) as e:
            await self.session.rollback()
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise ProductRepositoryException(
                operation="excluir",
                details=str(e),
            )

        return result.rowcount > 0

    async def get_active(self) -> List[ProductEntity]:
        """Lista produtos ativos."""
        try:
            result = await self.session.execute(
                select(ProductModel)
                .where(ProductModel.is_active)
                .order_by(ProductModel.name)
            )
            models = result.scalars().all()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="listar ativos",
                details=str(e),
            )

        return [ProductMapper.to_entity(model) for model in models]

    async def search_by_name(self, name: str) -> List[ProductEntity]:
        """Busca produtos por nome (parcial)."""
        try:
            result = await self.session.execute(
                select(ProductModel)
                .where(ProductModel.name.ilike(f"%{name}%"))
                .order_by(ProductModel.name)
            )
            models = result.scalars().all()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="buscar por nome",
                details=str(e),
            )

        return [ProductMapper.to_entity(model) for model in models]

    async def count(self) -> int:
        """Conta o total de produtos."""
        try:
            result = await self.session.execute(
                select(func.count()).select_from(ProductModel)
            )
            return result.scalar()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="contar",
                details=str(e),
            )

    async def count_by_category(self, category_id: str) -> int:
        """Conta produtos de uma categoria."""
        try:
            result = await self.session.execute(
                select(func.count())
                .select_from(ProductModel)
                .where(ProductModel.category_id == category_id)
            )
            return result.scalar()

        except (DBAPIError, ConnectionRefusedError) as e:
            raise ProductDatabaseConnectionException(details=str(e))

        except SQLAlchemyError as e:
            raise ProductRepositoryException(
                operation="contar por categoria",
                details=str(e),
            )

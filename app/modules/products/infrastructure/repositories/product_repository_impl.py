from typing import Optional, List
from decimal import Decimal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func

from ..models.product_model import ProductModel
from ...domain.entities.product_entity import ProductEntity
from ...domain.repositories.product_repository import ProductRepositoryInterface


class ProductRepositoryImpl(ProductRepositoryInterface):
    """Implementação do repositório de produtos usando SQLAlchemy"""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_entity(self, model: ProductModel) -> ProductEntity:
        """Converte modelo para entidade de domínio"""
        return ProductEntity(
            id=str(model.id),
            name=model.name,
            description=model.description,
            price=Decimal(str(model.price)),
            sku=model.sku,
            category_id=str(model.category_id),
            stock_quantity=model.stock_quantity,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: ProductEntity) -> ProductModel:
        """Converte entidade de domínio para modelo"""
        return ProductModel(
            id=entity.id,
            name=entity.name,
            description=entity.description,
            price=entity.price,
            sku=entity.sku,
            category_id=entity.category_id,
            stock_quantity=entity.stock_quantity,
            is_active=entity.is_active
        )

    async def create(self, entity: ProductEntity) -> ProductEntity:
        """Cria um novo produto no banco de dados"""
        model = self._to_model(entity)
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return self._to_entity(model)

    async def get_by_id(self, product_id: str) -> Optional[ProductEntity]:
        """Busca produto por ID"""
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_by_sku(self, sku: str) -> Optional[ProductEntity]:
        """Busca produto por SKU"""
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.sku == sku)
        )
        model = result.scalar_one_or_none()
        return self._to_entity(model) if model else None

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductEntity]:
        """Lista todos os produtos com paginação"""
        result = await self.session.execute(
            select(ProductModel)
            .order_by(ProductModel.name)
            .offset(skip)
            .limit(limit)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def get_by_category(self, category_id: str) -> List[ProductEntity]:
        """Lista produtos de uma categoria"""
        result = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.category_id == category_id)
            .order_by(ProductModel.name)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def update(self, entity: ProductEntity) -> ProductEntity:
        """Atualiza um produto"""
        result = await self.session.execute(
            select(ProductModel).where(ProductModel.id == entity.id)
        )
        model = result.scalar_one_or_none()

        if model:
            model.name = entity.name
            model.description = entity.description
            model.price = entity.price
            model.sku = entity.sku
            model.category_id = entity.category_id
            model.stock_quantity = entity.stock_quantity
            model.is_active = entity.is_active

            await self.session.commit()
            await self.session.refresh(model)
            return self._to_entity(model)

        return None

    async def delete(self, product_id: str) -> bool:
        """Exclui um produto pelo ID"""
        result = await self.session.execute(
            delete(ProductModel).where(ProductModel.id == product_id)
        )
        await self.session.commit()
        return result.rowcount > 0

    async def get_active(self) -> List[ProductEntity]:
        """Lista produtos ativos"""
        result = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.is_active)
            .order_by(ProductModel.name)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def search_by_name(self, name: str) -> List[ProductEntity]:
        """Busca produtos por nome (parcial)"""
        result = await self.session.execute(
            select(ProductModel)
            .where(ProductModel.name.ilike(f"%{name}%"))
            .order_by(ProductModel.name)
        )
        models = result.scalars().all()
        return [self._to_entity(model) for model in models]

    async def count(self) -> int:
        """Conta total de produtos"""
        result = await self.session.execute(
            select(func.count()).select_from(ProductModel)
        )
        return result.scalar()

    async def count_by_category(self, category_id: str) -> int:
        """Conta produtos de uma categoria"""
        result = await self.session.execute(
            select(func.count())
            .select_from(ProductModel)
            .where(ProductModel.category_id == category_id)
        )
        return result.scalar()

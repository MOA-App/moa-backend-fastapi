from app.modules.products.domain.entities.product_entity import ProductEntity
from app.modules.products.infrastructure.models.product_model import ProductModel
from app.modules.products.infrastructure.exceptions.product_infra_exceptions import (
    ProductMappingException,
)


class ProductMapper:
    """Responsável por converter ProductEntity <-> ProductModel."""

    @staticmethod
    def to_entity(model: ProductModel) -> ProductEntity:
        try:
            return ProductEntity(
                id=str(model.id),
                name=model.name,
                description=model.description,
                price=model.price,
                sku=model.sku,
                category_id=str(model.category_id),
                stock_quantity=model.stock_quantity,
                is_active=model.is_active,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        except Exception as e:
            raise ProductMappingException(details=str(e))

    @staticmethod
    def to_model(entity: ProductEntity) -> ProductModel:
        try:
            return ProductModel(
                id=entity.id,
                name=entity.name,
                description=entity.description,
                price=entity.price,
                sku=entity.sku,
                category_id=entity.category_id,
                stock_quantity=entity.stock_quantity,
                is_active=entity.is_active,
            )
        except Exception as e:
            raise ProductMappingException(details=str(e))

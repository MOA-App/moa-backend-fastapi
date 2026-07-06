from app.modules.products.domain.entities.category_entity import CategoryEntity
from app.modules.products.infrastructure.models.category_model import CategoryModel
from app.modules.products.infrastructure.exceptions.category_infra_exceptions import (
    CategoryMappingException,
)


class CategoryMapper:
    """Responsável por converter CategoryEntity <-> CategoryModel."""

    @staticmethod
    def to_entity(model: CategoryModel) -> CategoryEntity:
        try:
            return CategoryEntity(
                id=str(model.id),
                name=model.name,
                description=model.description,
                created_at=model.created_at,
                updated_at=model.updated_at,
            )
        except Exception as e:
            raise CategoryMappingException(details=str(e))

    @staticmethod
    def to_model(entity: CategoryEntity) -> CategoryModel:
        try:
            return CategoryModel(
                id=entity.id,
                name=entity.name,
                description=entity.description,
            )
        except Exception as e:
            raise CategoryMappingException(details=str(e))

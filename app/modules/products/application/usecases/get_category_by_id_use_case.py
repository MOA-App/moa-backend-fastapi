from typing import Optional

from ..dtos.category_dto import CategoryResponseDTO
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.category_exceptions import CategoryNotFoundException


class GetCategoryByIdUseCase:
    """Caso de uso para buscar categoria por ID"""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    async def execute(self, category_id: str) -> CategoryResponseDTO:
        """
        Busca uma categoria pelo seu ID.

        Args:
            category_id: ID da categoria

        Returns:
            CategoryResponseDTO: Dados da categoria encontrada

        Raises:
            CategoryNotFoundException: Se a categoria não for encontrada
        """
        category = await self.repository.get_by_id(category_id)

        if not category:
            raise CategoryNotFoundException(
                f"Categoria com ID '{category_id}' não encontrada"
            )

        return CategoryResponseDTO.model_validate(category)

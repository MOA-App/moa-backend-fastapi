from typing import List

from ..dtos.category_dto import CategoryResponseDTO
from ...domain.repositories.category_repository import CategoryRepositoryInterface


class ListCategoriesUseCase:
    """Caso de uso para listar todas as categorias"""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    async def execute(self) -> List[CategoryResponseDTO]:
        # Buscar todas as categorias
        categories = await self.repository.get_all()

        # Retornar lista de DTOs
        return [CategoryResponseDTO.model_validate(category) for category in categories]


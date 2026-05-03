
from ..dtos.category_dto import CategoryResponseDTO
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.category_exceptions import CategoryNotFoundException


class GetCategoryByNameUseCase:
    """Caso de uso para buscar categoria por nome"""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    async def execute(self, name: str) -> CategoryResponseDTO:
        """
        Busca uma categoria pelo seu nome.

        Args:
            name: Nome da categoria

        Returns:
            CategoryResponseDTO: Dados da categoria encontrada

        Raises:
            CategoryNotFoundException: Se a categoria não for encontrada
        """
        category = await self.repository.get_by_name(name)

        if not category:
            raise CategoryNotFoundException(
                f"Categoria com nome '{name}' não encontrada"
            )

        return CategoryResponseDTO.model_validate(category)


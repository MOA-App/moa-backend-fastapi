from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.category_exceptions import CategoryNotFoundException


class DeleteCategoryUseCase:
    """Caso de uso para excluir categoria"""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    async def execute(self, category_id: str) -> bool:
        # Verificar se categoria existe
        existing = await self.repository.get_by_id(category_id)
        if not existing:
            raise CategoryNotFoundException(f"Categoria com ID '{category_id}' não encontrada")

        # Excluir do repositório
        deleted = await self.repository.delete(category_id)

        return deleted


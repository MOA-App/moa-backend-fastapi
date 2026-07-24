from ..dtos.category_dto import CategoryCreateDTO, CategoryResponseDTO
from ...domain.entities.category_entity import CategoryEntity
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.category_exceptions import CategoryAlreadyExistsException


class CreateCategoryUseCase:
    """Caso de uso para criar categoria"""

    def __init__(self, repository: CategoryRepositoryInterface):
        self.repository = repository

    async def execute(self, data: CategoryCreateDTO) -> CategoryResponseDTO:
        # Verificar se categoria já existe
        existing = await self.repository.get_by_name(data.name)
        if existing:
            raise CategoryAlreadyExistsException(f"Categoria '{data.name}' já existe")

        # Criar entidade
        entity = CategoryEntity(
            id=None,  # Será gerado automaticamente
            name=data.name,
            description=data.description,
        )

        # Salvar no repositório
        created = await self.repository.create(entity)

        # Retornar DTO
        return CategoryResponseDTO.model_validate(created)

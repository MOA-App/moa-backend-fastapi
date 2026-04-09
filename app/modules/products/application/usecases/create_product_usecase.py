from ..dtos.create_product_dto import CreateProductDTO
from ..dtos.product_response_dto import ProductResponseDTO
from ...domain.entities.product_entity import ProductEntity
from ...domain.repositories.product_repository import ProductRepositoryInterface
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.product_exceptions import ProductAlreadyExistsException
from ...domain.exceptions.category_exceptions import CategoryNotFoundException


class CreateProductUseCase:
    """Caso de uso para criar produto"""

    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        category_repository: CategoryRepositoryInterface
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, data: CreateProductDTO) -> ProductResponseDTO:
        """
        Cria um novo produto.

        Args:
            data: Dados do produto a ser criado

        Returns:
            ProductResponseDTO: Dados do produto criado

        Raises:
            ProductAlreadyExistsException: Se já existe produto com o mesmo SKU
            CategoryNotFoundException: Se a categoria não existe
        """
        # Verificar se já existe produto com o mesmo SKU
        existing = await self.product_repository.get_by_sku(data.sku)
        if existing:
            raise ProductAlreadyExistsException(
                f"Produto com SKU '{data.sku}' já existe"
            )

        # Verificar se a categoria existe
        category = await self.category_repository.get_by_id(data.category_id)
        if not category:
            raise CategoryNotFoundException(
                f"Categoria com ID '{data.category_id}' não encontrada"
            )

        # Criar entidade
        entity = ProductEntity(
            id=None,
            name=data.name,
            description=data.description,
            price=data.price,
            sku=data.sku,
            category_id=data.category_id,
            stock_quantity=data.stock_quantity,
            is_active=data.is_active
        )

        # Salvar no repositório
        created = await self.product_repository.create(entity)

        # Retornar DTO
        return ProductResponseDTO.model_validate(created)


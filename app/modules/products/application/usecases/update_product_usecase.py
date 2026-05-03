from ..dtos.create_product_dto import UpdateProductDTO
from ..dtos.product_response_dto import ProductResponseDTO
from ...domain.repositories.product_repository import ProductRepositoryInterface
from ...domain.repositories.category_repository import CategoryRepositoryInterface
from ...domain.exceptions.product_exceptions import ProductNotFoundException, ProductAlreadyExistsException
from ...domain.exceptions.category_exceptions import CategoryNotFoundException


class UpdateProductUseCase:
    """Caso de uso para atualizar produto"""

    def __init__(
        self,
        product_repository: ProductRepositoryInterface,
        category_repository: CategoryRepositoryInterface
    ):
        self.product_repository = product_repository
        self.category_repository = category_repository

    async def execute(self, product_id: str, data: UpdateProductDTO) -> ProductResponseDTO:
        """
        Atualiza um produto existente.

        Args:
            product_id: ID do produto a ser atualizado
            data: Dados a serem atualizados

        Returns:
            ProductResponseDTO: Dados do produto atualizado

        Raises:
            ProductNotFoundException: Se o produto não for encontrado
            ProductAlreadyExistsException: Se o novo SKU já existe
            CategoryNotFoundException: Se a nova categoria não existe
        """
        # Buscar produto existente
        product = await self.product_repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(
                f"Produto com ID '{product_id}' não encontrado"
            )

        # Verificar se o novo SKU já existe (se estiver sendo alterado)
        if data.sku and data.sku != product.sku:
            existing = await self.product_repository.get_by_sku(data.sku)
            if existing:
                raise ProductAlreadyExistsException(
                    f"Produto com SKU '{data.sku}' já existe"
                )

        # Verificar se a nova categoria existe (se estiver sendo alterada)
        if data.category_id and data.category_id != product.category_id:
            category = await self.category_repository.get_by_id(data.category_id)
            if not category:
                raise CategoryNotFoundException(
                    f"Categoria com ID '{data.category_id}' não encontrada"
                )

        # Atualizar campos
        if data.name is not None:
            product.name = data.name
        if data.description is not None:
            product.description = data.description
        if data.price is not None:
            product.price = data.price
        if data.sku is not None:
            product.sku = data.sku
        if data.category_id is not None:
            product.category_id = data.category_id
        if data.stock_quantity is not None:
            product.stock_quantity = data.stock_quantity
        if data.is_active is not None:
            product.is_active = data.is_active

        # Salvar alterações
        updated = await self.product_repository.update(product)

        return ProductResponseDTO.model_validate(updated)


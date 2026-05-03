from ..dtos.product_response_dto import ProductResponseDTO
from ...domain.repositories.product_repository import ProductRepositoryInterface
from ...domain.exceptions.product_exceptions import ProductNotFoundException


class GetProductBySkuUseCase:
    """Caso de uso para buscar produto por SKU"""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    async def execute(self, sku: str) -> ProductResponseDTO:
        """
        Busca um produto pelo SKU.

        Args:
            sku: Código SKU do produto

        Returns:
            ProductResponseDTO: Dados do produto encontrado

        Raises:
            ProductNotFoundException: Se o produto não for encontrado
        """
        product = await self.repository.get_by_sku(sku)

        if not product:
            raise ProductNotFoundException(
                f"Produto com SKU '{sku}' não encontrado"
            )

        return ProductResponseDTO.model_validate(product)


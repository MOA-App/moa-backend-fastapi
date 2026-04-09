from ..dtos.product_response_dto import ProductResponseDTO
from ...domain.repositories.product_repository import ProductRepositoryInterface
from ...domain.exceptions.product_exceptions import ProductNotFoundException


class GetProductByIdUseCase:
    """Caso de uso para buscar produto por ID"""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    async def execute(self, product_id: str) -> ProductResponseDTO:
        """
        Busca um produto pelo ID.

        Args:
            product_id: ID do produto

        Returns:
            ProductResponseDTO: Dados do produto encontrado

        Raises:
            ProductNotFoundException: Se o produto não for encontrado
        """
        product = await self.repository.get_by_id(product_id)

        if not product:
            raise ProductNotFoundException(
                f"Produto com ID '{product_id}' não encontrado"
            )

        return ProductResponseDTO.model_validate(product)

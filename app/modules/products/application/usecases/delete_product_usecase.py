from ...domain.repositories.product_repository import ProductRepositoryInterface
from ...domain.exceptions.product_exceptions import ProductNotFoundException


class DeleteProductUseCase:
    """Caso de uso para excluir produto"""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    async def execute(self, product_id: str) -> bool:
        """
        Exclui um produto pelo ID.

        Args:
            product_id: ID do produto a ser excluído

        Returns:
            bool: True se excluído com sucesso

        Raises:
            ProductNotFoundException: Se o produto não for encontrado
        """
        # Verificar se o produto existe
        product = await self.repository.get_by_id(product_id)
        if not product:
            raise ProductNotFoundException(
                f"Produto com ID '{product_id}' não encontrado"
            )

        # Excluir produto
        return await self.repository.delete(product_id)


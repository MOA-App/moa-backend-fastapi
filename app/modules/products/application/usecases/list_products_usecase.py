from typing import List, Optional

from ..dtos.product_response_dto import ProductResponseDTO
from ...domain.repositories.product_repository import ProductRepositoryInterface


class ListProductsUseCase:
    """Caso de uso para listar produtos"""

    def __init__(self, repository: ProductRepositoryInterface):
        self.repository = repository

    async def execute(
        self,
        skip: int = 0,
        limit: int = 100,
        category_id: Optional[str] = None,
        active_only: bool = False
    ) -> List[ProductResponseDTO]:
        """
        Lista produtos com filtros opcionais.

        Args:
            skip: Número de registros a pular (paginação)
            limit: Limite de registros a retornar
            category_id: Filtrar por categoria
            active_only: Se True, retorna apenas produtos ativos

        Returns:
            List[ProductResponseDTO]: Lista de produtos
        """
        if category_id:
            products = await self.repository.get_by_category(category_id)
        elif active_only:
            products = await self.repository.get_active()
        else:
            products = await self.repository.get_all(skip=skip, limit=limit)

        return [ProductResponseDTO.model_validate(p) for p in products]

    async def search_by_name(self, name: str) -> List[ProductResponseDTO]:
        """
        Busca produtos por nome.

        Args:
            name: Nome ou parte do nome do produto

        Returns:
            List[ProductResponseDTO]: Produtos encontrados
        """
        products = await self.repository.search_by_name(name)
        return [ProductResponseDTO.model_validate(p) for p in products]

    async def count(self) -> int:
        """Retorna o total de produtos"""
        return await self.repository.count()

    async def count_by_category(self, category_id: str) -> int:
        """Retorna o total de produtos de uma categoria"""
        return await self.repository.count_by_category(category_id)


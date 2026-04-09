from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.product_entity import ProductEntity


class ProductRepositoryInterface(ABC):
    """Interface do repositório de produtos"""

    @abstractmethod
    async def create(self, entity: ProductEntity) -> ProductEntity:
        """Cria um novo produto"""
        pass

    @abstractmethod
    async def get_by_id(self, product_id: str) -> Optional[ProductEntity]:
        """Busca produto por ID"""
        pass

    @abstractmethod
    async def get_by_sku(self, sku: str) -> Optional[ProductEntity]:
        """Busca produto por SKU"""
        pass

    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ProductEntity]:
        """Lista todos os produtos com paginação"""
        pass

    @abstractmethod
    async def get_by_category(self, category_id: str) -> List[ProductEntity]:
        """Lista produtos de uma categoria"""
        pass

    @abstractmethod
    async def update(self, entity: ProductEntity) -> ProductEntity:
        """Atualiza um produto"""
        pass

    @abstractmethod
    async def delete(self, product_id: str) -> bool:
        """Exclui um produto pelo ID"""
        pass

    @abstractmethod
    async def get_active(self) -> List[ProductEntity]:
        """Lista produtos ativos"""
        pass

    @abstractmethod
    async def search_by_name(self, name: str) -> List[ProductEntity]:
        """Busca produtos por nome (parcial)"""
        pass

    @abstractmethod
    async def count(self) -> int:
        """Conta total de produtos"""
        pass

    @abstractmethod
    async def count_by_category(self, category_id: str) -> int:
        """Conta produtos de uma categoria"""
        pass


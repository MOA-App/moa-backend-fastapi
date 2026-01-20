from abc import ABC, abstractmethod
from typing import Optional, List
from ..entities.category_entity import CategoryEntity


class CategoryRepositoryInterface(ABC):
    """Interface do repositório de categorias"""

    @abstractmethod
    async def create(self, entity: CategoryEntity) -> CategoryEntity:
        """Cria uma nova categoria"""
        pass

    @abstractmethod
    async def get_by_id(self, category_id: str) -> Optional[CategoryEntity]:
        """Busca categoria por ID"""
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[CategoryEntity]:
        """Busca categoria por nome"""
        pass

    @abstractmethod
    async def get_all(self) -> List[CategoryEntity]:
        """Lista todas as categorias"""
        pass

    @abstractmethod
    async def delete(self, category_id: str) -> bool:
        """Exclui uma categoria pelo ID"""
        pass

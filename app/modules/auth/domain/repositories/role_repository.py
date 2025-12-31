from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.role_entity import Role
from ..value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId


class RoleRepository(ABC):
    """Interface do Repository de Role"""
    
    @abstractmethod
    async def create(self, role: Role) -> Role:
        """Cria uma nova role"""
        pass
    
    @abstractmethod
    async def find_by_id(self, role_id: EntityId) -> Optional[Role]:
        """Busca role por ID"""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: RoleName) -> Optional[Role]:
        """Busca role por nome"""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: RoleName) -> bool:
        """Verifica se existe role com o nome informado"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Role]:
        """Lista todas as roles"""
        pass
    
    @abstractmethod
    async def update(self, role: Role) -> Role:
        """Atualiza uma role"""
        pass
    
    @abstractmethod
    async def delete(self, role_id: EntityId) -> bool:
        """Deleta uma role"""
        pass
    
    @abstractmethod
    async def add_permission_to_role(self, role_id: EntityId, permission_id: EntityId) -> bool:
        """Adiciona uma permissão a uma role"""
        pass
    
    @abstractmethod
    async def remove_permission_from_role(self, role_id: EntityId, permission_id: EntityId) -> bool:
        """Remove uma permissão de uma role"""
        pass

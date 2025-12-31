from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.permission_entity import Permission
from ..value_objects.permission_name_vo import PermissionName
from app.shared.domain.value_objects.id_vo import EntityId


class PermissionRepository(ABC):
    """Interface do Repository de Permission"""
    
    @abstractmethod
    async def create(self, permission: Permission) -> Permission:
        """Cria uma nova permissão"""
        pass
    
    @abstractmethod
    async def find_by_id(self, permission_id: EntityId) -> Optional[Permission]:
        """Busca permissão por ID"""
        pass
    
    @abstractmethod
    async def find_by_name(self, name: PermissionName) -> Optional[Permission]:
        """Busca permissão por nome"""
        pass
    
    @abstractmethod
    async def exists_by_name(self, name: PermissionName) -> bool:
        """Verifica se existe permissão com o nome informado"""
        pass
    
    @abstractmethod
    async def list_all(self) -> List[Permission]:
        """Lista todas as permissões"""
        pass
    
    @abstractmethod
    async def list_by_resource(self, resource: str) -> List[Permission]:
        """Lista permissões por recurso (ex: 'users')"""
        pass
    
    @abstractmethod
    async def update(self, permission: Permission) -> Permission:
        """Atualiza uma permissão"""
        pass
    
    @abstractmethod
    async def delete(self, permission_id: EntityId) -> bool:
        """Deleta uma permissão"""
        pass

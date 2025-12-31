from dataclasses import dataclass, field
from typing import List

from ..value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId


@dataclass
class Role:
    """Entidade Role (Função/Papel) do Domínio"""
    id: EntityId
    nome: RoleName
    permissions: List['Permission'] = field(default_factory=list)
    
    @staticmethod
    def create(nome: str) -> 'Role':
        """Factory method para criar uma nova role"""
        return Role(
            id=EntityId.generate(),
            nome=RoleName(nome),
            permissions=[]
        )
    
    @staticmethod
    def reconstruct(
        id: EntityId,
        nome: RoleName,
        permissions: List['Permission']
    ) -> 'Role':
        """Reconstrói uma role existente"""
        return Role(
            id=id,
            nome=nome,
            permissions=permissions
        )
    
    # Métodos de Permissions
    def add_permission(self, permission: 'Permission') -> None:
        """Adiciona uma permissão à role"""
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def remove_permission(self, permission: 'Permission') -> None:
        """Remove uma permissão da role"""
        if permission in self.permissions:
            self.permissions.remove(permission)
    
    def has_permission(self, permission_name: str) -> bool:
        """Verifica se a role tem uma permissão específica"""
        return any(
            p.nome.value == permission_name.lower() 
            for p in self.permissions
        )
    
    def get_permission_names(self) -> List[str]:
        """Retorna lista com nomes das permissões"""
        return [p.nome.value for p in self.permissions]
    
    def get_permissions_by_resource(self, resource: str) -> List['Permission']:
        """Retorna permissões de um recurso específico"""
        return [
            p for p in self.permissions 
            if p.get_resource() == resource.lower()
        ]
    
    def clear_permissions(self) -> None:
        """Remove todas as permissões"""
        self.permissions.clear()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Role):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)

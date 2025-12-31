from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from ..value_objects.permission_name_vo import PermissionName
from app.shared.domain.value_objects.id_vo import EntityId


@dataclass
class Permission:
    """Entidade Permission (Permissão) do Domínio"""
    id: EntityId
    nome: PermissionName
    descricao: Optional[str]
    data_criacao: datetime
    
    @staticmethod
    def create(nome: str, descricao: Optional[str] = None) -> 'Permission':
        """Factory method para criar uma nova permissão"""
        return Permission(
            id=EntityId.generate(),
            nome=PermissionName(nome),
            descricao=descricao,
            data_criacao=datetime.utcnow()
        )
    
    @staticmethod
    def reconstruct(
        id: EntityId,
        nome: PermissionName,
        descricao: Optional[str],
        data_criacao: datetime
    ) -> 'Permission':
        """Reconstrói uma permissão existente"""
        return Permission(
            id=id,
            nome=nome,
            descricao=descricao,
            data_criacao=data_criacao
        )
    
    def get_resource(self) -> str:
        """
        Retorna o recurso da permissão.
        Ex: 'users.create' -> 'users'
        """
        return self.nome.get_resource()
    
    def get_action(self) -> str:
        """
        Retorna a ação da permissão.
        Ex: 'users.create' -> 'create'
        """
        return self.nome.get_action()
    
    def update_description(self, new_description: str) -> None:
        """Atualiza a descrição da permissão"""
        self.descricao = new_description
    
    def is_for_resource(self, resource: str) -> bool:
        """Verifica se a permissão é para um recurso específico"""
        return self.get_resource() == resource.lower()
    
    def is_action(self, action: str) -> bool:
        """Verifica se a permissão representa uma ação específica"""
        return self.get_action() == action.lower()
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Permission):
            return False
        return self.id == other.id
    
    def __hash__(self) -> int:
        return hash(self.id)
    
    def __str__(self) -> str:
        return f"Permission({self.nome.value})"

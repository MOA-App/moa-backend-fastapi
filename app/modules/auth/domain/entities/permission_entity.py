from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional

from app.shared.domain.value_objects.id_vo import EntityId
from ..value_objects.permission_name_vo import PermissionName


@dataclass(frozen=True, eq=False)  # ← Tornar imutável
class Permission:
    """
    Entidade Permission do Domínio.
    
    Representa uma permissão granular no sistema RBAC.
    Formato: resource.action (ex: users.create, posts.delete)
    """
    
    id: EntityId
    nome: PermissionName
    descricao: Optional[str]
    data_criacao: datetime

    @classmethod
    def create(cls, nome: str, descricao: Optional[str] = None) -> "Permission":
        """Factory method para criar nova permissão"""
        return cls(
            id=EntityId.generate(),
            nome=PermissionName(nome),
            descricao=descricao,
            data_criacao=datetime.now(timezone.utc),
        )

    @classmethod
    def reconstruct(
        cls,
        id: EntityId,
        nome: PermissionName,
        descricao: Optional[str],
        data_criacao: datetime,
    ) -> "Permission":
        """Reconstrói permissão existente (usado pelos repositories)"""
        return cls(id=id, nome=nome, descricao=descricao, data_criacao=data_criacao)

    # ---------- Behavior ----------
    
    def update_description(self, new_description: Optional[str]) -> "Permission":
        """
        Atualiza descrição (retorna nova instância por ser imutável).
        
        Returns:
            Permission: Nova instância com descrição atualizada
        """
        return replace(self, descricao=new_description)
    
    def change_name(self, new_name: str) -> "Permission":
        """
        Altera nome da permissão (retorna nova instância).
        
        Args:
            new_name: Novo nome no formato resource.action
            
        Returns:
            Permission: Nova instância com nome atualizado
        """
        return replace(self, nome=PermissionName(new_name))

    def is_for_resource(self, resource: str) -> bool:
        """Verifica se permissão pertence a um recurso específico"""
        return self.nome.get_resource() == resource.lower()

    def is_action(self, action: str) -> bool:
        """Verifica se permissão representa uma ação específica"""
        return self.nome.get_action() == action.lower()
    
    def matches(self, pattern: str) -> bool:
        """
        Verifica se permissão corresponde a um padrão.
        
        Examples:
            permission.matches("users.*")  # Qualquer ação de users
            permission.matches("*.create")  # Qualquer criação
            permission.matches("users.create")  # Exato
        """
        if "*" not in pattern:
            return self.nome.value == pattern.lower()
        
        resource_pattern, action_pattern = pattern.lower().split(".", 1)
        
        resource_match = (
            resource_pattern == "*" or 
            self.nome.get_resource() == resource_pattern
        )
        action_match = (
            action_pattern == "*" or 
            self.nome.get_action() == action_pattern
        )
        
        return resource_match and action_match
    
    def get_full_name(self) -> str:
        """Retorna nome completo da permissão"""
        return self.nome.value
    
    def get_resource(self) -> str:
        """Retorna recurso da permissão"""
        return self.nome.get_resource()
    
    def get_action(self) -> str:
        """Retorna ação da permissão"""
        return self.nome.get_action()

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        """Igualdade baseada no ID (identidade)"""
        return isinstance(other, Permission) and self.id == other.id

    def __hash__(self) -> int:
        """Hash baseado no ID para uso em sets/dicts"""
        return hash(self.id)

    def __str__(self) -> str:
        """Representação string amigável"""
        return f"Permission({self.nome.value})"
    
    def __repr__(self) -> str:
        """Representação para debugging"""
        return (
            f"Permission(id={self.id}, nome={self.nome.value}, "
            f"descricao={self.descricao!r})"
        )

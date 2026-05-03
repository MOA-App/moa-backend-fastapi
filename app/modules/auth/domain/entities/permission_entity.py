from dataclasses import dataclass, replace
from datetime import datetime, timezone
from typing import Optional

from app.modules.auth.domain.value_objects.permission_resource_vo import PermissionResource
from app.shared.domain.value_objects.id_vo import EntityId
from ..value_objects.permission_name_vo import PermissionName

@dataclass(frozen=True, eq=False)
class Permission:
    """
    Entidade de domínio que representa uma permissão no sistema (RBAC).
    Uma permissão define uma ação permitida sobre um recurso específico,
    seguindo o formato padrão: `<resource>.<action>`.
    """

    id: EntityId
    nome: PermissionName
    descricao: Optional[str]
    data_criacao: datetime

    @classmethod
    def create(
        cls,
        nome: PermissionName,
        descricao: Optional[str] = None
    ) -> "Permission":
        """
        Cria uma nova permissão.
        """
        return cls(
            id=EntityId.generate(),
            nome=nome,
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
        """
        Reconstrói uma permissão existente a partir de dados persistidos.
        """
        return cls(id=id, nome=nome, descricao=descricao, data_criacao=data_criacao)

    # ---------- Behavior ----------
    
    def update_description(self, new_description: Optional[str]) -> "Permission":
        """
        Atualiza a descrição da permissão.
        """
        return replace(self, descricao=new_description)

    def is_for_resource(self, resource: PermissionResource) -> bool:
        """
        Verifica se a permissão pertence a um recurso específico.
        """
        return self.nome.resource == resource

    def is_action(self, action: str) -> bool:
        """
        Verifica se a permissão representa uma ação específica.
        """
        return self.nome.action == action.lower()
    
    def matches(self, pattern: str) -> bool:
        """
        Verifica se a permissão corresponde a um padrão com wildcard (*).
        """
        if "*" not in pattern:
            return self.nome.value == pattern.lower()
        
        resource_pattern, action_pattern = pattern.lower().split(".", 1)
        
        resource_match = (
            resource_pattern == "*" or 
            self.nome.resource.value == resource_pattern
        )
        action_match = (
            action_pattern == "*" or 
            self.nome.action == action_pattern
        )
        
        return resource_match and action_match
    
    def get_full_name(self) -> str:
        """
        Retorna o nome completo da permissão.
        """
        return self.nome.value
    
    def resource(self) -> str:
        """
        Retorna o recurso da permissão.
        """
        return self.nome.resource.value
    
    def action(self) -> str:
        """
        Retorna a ação da permissão.
        """
        return self.nome.action

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        """
        Define igualdade baseada na identidade (ID).
        """
        return isinstance(other, Permission) and self.id == other.id

    def __hash__(self) -> int:
        """
        Permite uso da entidade em sets e dicionários.
        """
        return hash(self.id)

    def __str__(self) -> str:
        """
        Representação amigável.
        """
        return f"Permission({self.nome.value})"
    
    def __repr__(self) -> str:
        """
        Representação detalhada para debugging.
        """
        return (
            f"Permission(id={self.id}, nome={self.nome.value}, "
            f"descricao={self.descricao!r})"
        )

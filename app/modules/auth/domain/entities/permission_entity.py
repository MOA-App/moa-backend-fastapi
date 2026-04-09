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

    Exemplos:
        - "users.create"
        - "posts.delete"
        - "orders.read"

    Características:
        - Imutável (frozen=True): qualquer alteração retorna uma nova instância.
        - Igualdade baseada em identidade (id).
        - Encapsula regras de comparação e matching de permissões.

    Attributes:
        id (EntityId): Identificador único da permissão.
        nome (PermissionName): Value Object contendo resource e action.
        descricao (Optional[str]): Descrição opcional da permissão.
        data_criacao (datetime): Data de criação em UTC.
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

        Gera automaticamente:
            - ID único
            - Data de criação em UTC

        Args:
            nome (PermissionName): Nome estruturado da permissão.
            descricao (Optional[str]): Descrição opcional.

        Returns:
            Permission: Nova instância de Permission.
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

        Usado principalmente por repositories ao carregar dados do banco.

        Args:
            id (EntityId): Identificador da permissão.
            nome (PermissionName): Nome estruturado.
            descricao (Optional[str]): Descrição.
            data_criacao (datetime): Data de criação original.

        Returns:
            Permission: Instância reconstruída.
        """
        return cls(id=id, nome=nome, descricao=descricao, data_criacao=data_criacao)

    # ---------- Behavior ----------
    
    def update_description(self, new_description: Optional[str]) -> "Permission":
        """
        Atualiza a descrição da permissão.

        Como a entidade é imutável, retorna uma nova instância com a alteração.

        Args:
            new_description (Optional[str]): Nova descrição.

        Returns:
            Permission: Nova instância atualizada.
        """
        return replace(self, descricao=new_description)

    def is_for_resource(self, resource: PermissionResource) -> bool:
        """
        Verifica se a permissão pertence a um recurso específico.

        Args:
            resource (PermissionResource): Recurso a ser comparado.

        Returns:
            bool: True se pertence ao recurso, False caso contrário.
        """
        return self.nome.resource == resource

    def is_action(self, action: str) -> bool:
        """
        Verifica se a permissão representa uma ação específica.

        Comparação é case-insensitive.

        Args:
            action (str): Nome da ação.

        Returns:
            bool: True se corresponde à ação.
        """
        return self.nome.action == action.lower()
    
    def matches(self, pattern: str) -> bool:
        """
        Verifica se a permissão corresponde a um padrão com wildcard (*).

        Regras:
            - "*" pode ser usado para representar qualquer resource ou action.
            - Comparação é case-insensitive.

        Exemplos:
            - "users.*"     → qualquer ação no recurso users
            - "*.create"    → qualquer recurso com ação create
            - "users.create" → correspondência exata

        Args:
            pattern (str): Padrão de comparação.

        Returns:
            bool: True se corresponder ao padrão.
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

        Returns:
            str: Nome no formato "resource.action".
        """
        return self.nome.value
    
    def resource(self) -> str:
        """
        Retorna o recurso da permissão.

        Returns:
            str: Nome do recurso.
        """
        return self.nome.resource.value
    
    def action(self) -> str:
        """
        Retorna a ação da permissão.

        Returns:
            str: Nome da ação.
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

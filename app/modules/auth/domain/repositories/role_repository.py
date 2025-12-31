from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.role_entity import Role
from ..value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId

class RoleRepository(ABC):
    """Interface do Repository de Role (Port)"""

    @abstractmethod
    async def create(self, role: Role) -> Role:
        """
        Cria uma nova role no banco de dados.

        Args:
            role: Entidade Role a ser persistida

        Returns:
            Role: Role criada com dados atualizados

        Raises:
            RoleAlreadyExistsException: Já existe uma role com o mesmo nome
            RepositoryException: Erro ao persistir no banco
        """
        pass

    @abstractmethod
    async def find_by_id(self, role_id: EntityId) -> Optional[Role]:
        """
        Busca uma role pelo ID.

        Args:
            role_id: ID da role

        Returns:
            Optional[Role]: Role encontrada ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: RoleName) -> Optional[Role]:
        """
        Busca uma role pelo nome.

        Args:
            name: Nome da role (Value Object)

        Returns:
            Optional[Role]: Role encontrada ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def exists_by_name(self, name: RoleName) -> bool:
        """
        Verifica se existe uma role com o nome informado.

        Args:
            name: Nome da role

        Returns:
            bool: True se existir, False caso contrário

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def list_all(self) -> List[Role]:
        """
        Lista todas as roles cadastradas.

        Returns:
            List[Role]: Lista de roles

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def update(self, role: Role) -> Role:
        """
        Atualiza os dados de uma role existente.

        Args:
            role: Entidade Role com dados atualizados

        Returns:
            Role: Role atualizada

        Raises:
            RoleNotFoundException: Role não encontrada
            RepositoryException: Erro ao atualizar no banco
        """
        pass

    @abstractmethod
    async def delete(self, role_id: EntityId) -> None:
        """
        Remove uma role do sistema.

        Args:
            role_id: ID da role a ser removida

        Raises:
            RoleNotFoundException: Role não encontrada
            RepositoryException: Erro ao deletar no banco
        """
        pass

    @abstractmethod
    async def add_permission_to_role(
        self,
        role_id: EntityId,
        permission_id: EntityId,
    ) -> bool:
        """
        Associa uma permissão a uma role.

        Args:
            role_id: ID da role
            permission_id: ID da permissão

        Returns:
            bool: True se a permissão foi adicionada com sucesso

        Raises:
            RoleNotFoundException: Role não encontrada
            PermissionNotFoundException: Permissão não encontrada
            RoleAlreadyAssignedException: Permissão já associada à role
            RepositoryException: Erro ao persistir no banco
        """
        pass

    @abstractmethod
    async def remove_permission_from_role(
        self,
        role_id: EntityId,
        permission_id: EntityId,
    ) -> bool:
        """
        Remove a associação de uma permissão de uma role.

        Args:
            role_id: ID da role
            permission_id: ID da permissão

        Returns:
            bool: True se a permissão foi removida com sucesso

        Raises:
            RoleNotFoundException: Role não encontrada
            PermissionNotFoundException: Permissão não encontrada
            RoleNotAssignedException: Permissão não está associada à role
            RepositoryException: Erro ao persistir no banco
        """
        pass

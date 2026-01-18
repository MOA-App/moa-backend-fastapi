from abc import ABC, abstractmethod
from typing import Optional, List

from ..entities.permission_entity import Permission
from ..value_objects.permission_name_vo import PermissionName
from app.shared.domain.value_objects.id_vo import EntityId


class PermissionRepository(ABC):
    """Interface do Repository de Permission (Port)"""

    @abstractmethod
    async def create(self, permission: Permission) -> Permission:
        """
        Cria uma nova permissão no banco de dados.

        Args:
            permission: Entidade Permission a ser persistida

        Returns:
            Permission: Permissão criada com dados atualizados

        Raises:
            PermissionAlreadyExistsException: Já existe permissão com o mesmo nome
            RepositoryException: Erro ao persistir no banco
        """
        pass

    @abstractmethod
    async def find_by_id(self, permission_id: EntityId) -> Optional[Permission]:
        """
        Busca permissão pelo ID.

        Args:
            permission_id: ID da permissão

        Returns:
            Optional[Permission]: Permissão encontrada ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def find_by_name(self, name: PermissionName) -> Optional[Permission]:
        """
        Busca permissão pelo nome.

        Args:
            name: Nome da permissão (Value Object)

        Returns:
            Optional[Permission]: Permissão encontrada ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def exists_by_name(self, name: PermissionName) -> bool:
        """
        Verifica se existe uma permissão com o nome informado.

        Args:
            name: Nome da permissão

        Returns:
            bool: True se existir, False caso contrário

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def list_all(self) -> List[Permission]:
        """
        Lista todas as permissões cadastradas.

        Returns:
            List[Permission]: Lista de permissões

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def list_by_resource(self, resource: str) -> List[Permission]:
        """
        Lista permissões associadas a um recurso específico
        (ex: 'users', 'roles').

        Args:
            resource: Nome do recurso

        Returns:
            List[Permission]: Lista de permissões do recurso

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def update(self, permission: Permission) -> Permission:
        """
        Atualiza os dados de uma permissão existente.

        Args:
            permission: Entidade Permission com dados atualizados

        Returns:
            Permission: Permissão atualizada

        Raises:
            PermissionNotFoundException: Permissão não encontrada
            RepositoryException: Erro ao atualizar no banco
        """
        pass

    @abstractmethod
    async def delete(self, permission_id: EntityId) -> None:
        """
        Remove uma permissão do sistema.

        Args:
            permission_id: ID da permissão a ser removida

        Raises:
            PermissionNotFoundException: Permissão não encontrada
            RepositoryException: Erro ao deletar no banco
        """
        pass

    @abstractmethod
    async def list_resources(self) -> List[str]:
        """Lista todos os recursos distintos"""
        pass


    @abstractmethod
    async def list_actions(self, resource: str) -> List[str]:
        """Lista ações disponíveis para um recurso"""
        pass

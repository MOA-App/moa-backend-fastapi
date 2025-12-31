from abc import ABC, abstractmethod
from typing import Optional

from ..entities.user_entity import User
from ..value_objects.email_vo import Email
from ..value_objects.username_vo import Username
from app.shared.domain.value_objects.id_vo import EntityId


class UserRepository(ABC):
    """Interface do Repository de User (Port)"""

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Persiste um novo usuário.

        Args:
            user: Entidade User validada

        Returns:
            User: Usuário persistido

        Raises:
            RepositoryException: Erro genérico de persistência
            DatabaseConnectionException: Falha de conexão com o banco
            DatabaseOperationException: Falha ao executar insert
        """
        pass

    @abstractmethod
    async def find_by_id(self, user_id: EntityId) -> Optional[User]:
        """
        Busca usuário por ID.

        Args:
            user_id: Identificador do usuário

        Returns:
            Optional[User]: Usuário encontrado ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """
        Busca usuário por email.

        Args:
            email: Email (Value Object)

        Returns:
            Optional[User]: Usuário encontrado ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def find_by_username(self, username: Username) -> Optional[User]:
        """
        Busca usuário por nome de usuário.

        Args:
            username: Username (Value Object)

        Returns:
            Optional[User]: Usuário encontrado ou None

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """
        Verifica existência de usuário por email.

        Args:
            email: Email a verificar

        Returns:
            bool: True se existir

        Raises:
            RepositoryException: Erro ao acessar o banco
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Atualiza um usuário existente.

        Args:
            user: Entidade User

        Returns:
            User: Usuário atualizado

        Raises:
            RepositoryException: Erro ao atualizar dados
        """
        pass

    @abstractmethod
    async def delete(self, user_id: EntityId) -> None:
        """
        Remove um usuário por ID.

        Args:
            user_id: Identificador do usuário

        Raises:
            RepositoryException: Erro ao deletar
        """
        pass

    @abstractmethod
    async def add_role_to_user(self, user_id: EntityId, role_id: EntityId) -> bool:
        """
        Associa uma role ao usuário.

        Args:
            user_id: ID do usuário
            role_id: ID da role

        Returns:
            bool: True se associação criada

        Raises:
            RepositoryException: Erro ao persistir associação
        """
        pass

    @abstractmethod
    async def remove_role_from_user(self, user_id: EntityId, role_id: EntityId) -> bool:
        """
        Remove associação entre usuário e role.

        Args:
            user_id: ID do usuário
            role_id: ID da role

        Returns:
            bool: True se associação removida

        Raises:
            RepositoryException: Erro ao remover associação
        """
        pass

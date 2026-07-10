from abc import ABC, abstractmethod
from typing import Optional, List

from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName

from ..entities.user_entity import User
from app.shared.domain.value_objects.id_vo import EntityId


class UserRepositoryInterface(ABC):
    """
    Contrato do repositório de usuários.
    """

    @abstractmethod
    async def create(self, user: User) -> User:
        """
        Persiste um novo usuário.
        """
        pass

    @abstractmethod
    async def update(self, user: User) -> User:
        """
        Atualiza um usuário.
        """
        pass

    @abstractmethod
    async def delete(self, user_id: EntityId) -> bool:
        """
        Remove um usuário.
        """
        pass

    @abstractmethod
    async def get_by_id(
        self,
        user_id: EntityId,
    ) -> Optional[User]:
        """
        Busca usuário pelo ID.
        """
        pass

    @abstractmethod
    async def get_by_email(
        self,
        email: Email,
    ) -> Optional[User]:
        """
        Busca usuário pelo e-mail.
        """
        pass

    @abstractmethod
    async def get_all(self) -> List[User]:
        """
        Lista todos os usuários.
        """
        pass

    @abstractmethod
    async def exists_by_email(
        self,
        email: Email,
    ) -> bool:
        """
        Verifica se existe um usuário com o e-mail informado.
        """
        pass

    @abstractmethod
    async def exists_by_id(
        self,
        user_id: EntityId,
    ) -> bool:
        """
        Verifica se o usuário existe.
        """
        pass

    @abstractmethod
    async def get_by_username(
        self,
        username: UserName,
    ) -> Optional[User]:
        """
        Busca usuário pelo nome.
        """
        pass

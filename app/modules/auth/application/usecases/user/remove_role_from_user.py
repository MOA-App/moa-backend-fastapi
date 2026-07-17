from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
    RoleNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.modules.auth.domain.repositories.role_repository import (
    RoleRepositoryInterface,
)
from app.shared.domain.value_objects.id_vo import EntityId


class RemoveRoleFromUserUseCase:
    """
    Caso de uso responsável por remover uma role de um usuário.
    """

    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        role_repository: RoleRepositoryInterface,
    ):
        self._user_repository = user_repository
        self._role_repository = role_repository

    async def execute(
        self,
        user_id: str,
        role_id: str,
    ) -> UserResponse:
        """
        Remove uma role do usuário.
        """

        user = await self._user_repository.get_by_id(
            EntityId.from_string(user_id)
        )

        if user is None:
            raise UserNotFoundException(
                f"User '{user_id}' not found."
            )

        role = await self._role_repository.get_by_id(
            EntityId.from_string(role_id)
        )

        if role is None:
            raise RoleNotFoundException(
                f"Role '{role_id}' not found."
            )

        user.remove_role(role)

        updated_user = await self._user_repository.update(user)

        return UserMapper.to_dto(updated_user)

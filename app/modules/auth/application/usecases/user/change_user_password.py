from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.exceptions.auth_exceptions import (
    InvalidPasswordException,
    UserNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.modules.auth.domain.services.password_hasher_interface import (
    PasswordHasherInterface,
)
from app.modules.auth.domain.value_objects.user_vo.user_password_vo import Password
from app.shared.domain.value_objects.id_vo import EntityId


class ChangeUserPasswordUseCase:
    """
    Caso de uso responsável por alterar a senha de um usuário.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
        password_hasher: PasswordHasherInterface,
    ):
        self._repository = repository
        self._password_hasher = password_hasher

    async def execute(
        self,
        user_id: str,
        current_password: str,
        new_password: str,
    ) -> UserResponse:
        """
        Altera a senha de um usuário.
        """

        entity_id = EntityId.from_string(user_id)

        user = await self._repository.get_by_id(entity_id)

        if user is None:
            raise UserNotFoundException(
                f"User '{user_id}' not found."
            )

        if not self._password_hasher.verify(
            current_password,
            user.password.value,
        ):
            raise InvalidPasswordException(
                "Current password is incorrect."
            )

        hashed_password = self._password_hasher.hash(
            new_password
        )

        user.change_password(
            Password(hashed_password)
        )

        updated_user = await self._repository.update(user)

        return UserMapper.to_dto(updated_user)

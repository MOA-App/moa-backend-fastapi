
from app.modules.auth.application.dtos.user.update_user_request_dto import UpdateUserRequest
from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.modules.auth.domain.services.password_hasher_interface import (
    PasswordHasherInterface,
)
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName
from app.modules.auth.domain.value_objects.user_vo.user_password_vo import Password
from app.shared.domain.value_objects.id_vo import EntityId


class UpdateUserUseCase:
    """
    Caso de uso responsável por atualizar um usuário.
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
        dto: UpdateUserRequest,
    ) -> UserResponse:
        """
        Atualiza os dados de um usuário.
        """

        entity_id = EntityId.from_string(user_id)

        user = await self._repository.get_by_id(entity_id)

        if user is None:
            raise UserNotFoundException(
                f"User '{user_id}' not found."
            )

        # Nome
        if dto.name is not None:
            user.change_name(
                UserName(dto.name)
            )

        # Email
        if dto.email is not None:
            new_email = Email(dto.email)

            existing_user = await self._repository.get_by_email(
                new_email
            )

            if (
                existing_user is not None
                and existing_user.id != user.id
            ):
                raise UserAlreadyExistsException(
                    f"User with email '{dto.email}' already exists."
                )

            user.change_email(new_email)

        # Senha
        if dto.password is not None:
            hashed_password = self._password_hasher.hash(
                dto.password
            )

            user.change_password(
                Password(hashed_password)
            )

        # Ativo/Inativo
        if dto.is_active is not None:
            if dto.is_active:
                user.activate()
            else:
                user.deactivate()

        updated_user = await self._repository.update(user)

        return UserMapper.to_dto(updated_user)

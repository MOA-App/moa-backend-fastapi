from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper
from app.modules.auth.domain.entities.user_entity import User
from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)

from app.modules.auth.domain.services.password_hasher_interface import PasswordHasherInterface
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName
from app.modules.auth.domain.value_objects.user_vo.user_password_vo import Password


class CreateUserUseCase:
    """
    Caso de uso responsável pela criação de usuários.
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
        name: str,
        email: str,
        password: str,
    ) -> UserResponse:
        """
        Cria um novo usuário.
        """

        email_vo = Email(email)

        if await self._repository.exists_by_email(email_vo):
            raise UserAlreadyExistsException(
                f"User with email '{email}' already exists."
            )

        hashed_password = self._password_hasher.hash(password)

        user = User.create(
            name=UserName(name),
            email=email_vo,
            password=Password(hashed_password),
        )

        created_user = await self._repository.create(user)

        return UserMapper.to_dto(created_user)

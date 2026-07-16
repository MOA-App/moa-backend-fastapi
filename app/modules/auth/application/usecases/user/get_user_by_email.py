
from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email


class GetUserByEmailUseCase:
    """
    Caso de uso responsável por buscar um usuário pelo e-mail.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self._repository = repository

    async def execute(
        self,
        email: str,
    ) -> UserResponse:
        """
        Busca um usuário pelo e-mail.
        """

        email_vo = Email(email)

        user = await self._repository.get_by_email(email_vo)

        if user is None:
            raise UserNotFoundException(
                f"User with email '{email}' not found."
            )

        return UserMapper.to_dto(user)

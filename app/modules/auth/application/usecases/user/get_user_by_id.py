
from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.shared.domain.value_objects.id_vo import EntityId


class GetUserByIdUseCase:
    """
    Caso de uso responsável por buscar um usuário pelo ID.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self._repository = repository

    async def execute(
        self,
        user_id: str,
    ) -> UserResponse:
        """
        Busca um usuário pelo ID.
        """

        entity_id = EntityId.from_string(user_id)

        user = await self._repository.get_by_id(entity_id)

        if user is None:
            raise UserNotFoundException(
                f"User '{user_id}' not found."
            )

        return UserMapper.to_dto(user)

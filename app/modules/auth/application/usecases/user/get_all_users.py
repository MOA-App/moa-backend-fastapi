from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.application.mappers.user_mapper import UserMapper

from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)


class GetAllUsersUseCase:
    """
    Caso de uso responsável por listar todos os usuários.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self._repository = repository

    async def execute(self) -> list[UserResponse]:
        """
        Retorna todos os usuários cadastrados.
        """

        users = await self._repository.get_all()

        return UserMapper.to_dto_list(users)

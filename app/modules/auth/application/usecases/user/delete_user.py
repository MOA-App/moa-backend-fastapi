from app.modules.auth.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
)
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.shared.domain.value_objects.id_vo import EntityId


class DeleteUserUseCase:
    """
    Caso de uso responsável por excluir um usuário.
    """

    def __init__(
        self,
        repository: UserRepositoryInterface,
    ):
        self._repository = repository

    async def execute(
        self,
        user_id: str,
    ) -> bool:
        """
        Exclui um usuário pelo ID.
        """

        entity_id = EntityId.from_string(user_id)

        user = await self._repository.get_by_id(entity_id)

        if user is None:
            raise UserNotFoundException(
                f"User '{user_id}' not found."
            )

        return await self._repository.delete(entity_id)

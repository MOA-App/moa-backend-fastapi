from uuid import UUID

from app.modules.auth.domain.exceptions.auth_exceptions import RoleNotFoundException
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.shared.domain.value_objects.id_vo import EntityId


class DeleteRoleUseCase:
    """Caso de uso para remoção de uma role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, role_id: UUID) -> None:
        """
        Remove uma role pelo ID.

        Args:
            role_id: UUID da role a ser removida

        Raises:
            RoleNotFoundException: Role não encontrada
        """
        entity_id = EntityId(role_id)
        role = await self._role_repository.find_by_id(entity_id)

        if role is None:
            raise RoleNotFoundException(f"Role com ID '{role_id}' não encontrada.")

        await self._role_repository.delete(entity_id)

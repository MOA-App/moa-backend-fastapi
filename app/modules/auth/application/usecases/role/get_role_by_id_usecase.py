from uuid import UUID

from app.modules.auth.application.dtos.role.role_outputs import RoleResponseDTO
from app.modules.auth.application.mappers.role_mapper import to_role_response_dto
from app.modules.auth.domain.exceptions.auth_exceptions import RoleNotFoundException
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.shared.domain.value_objects.id_vo import EntityId


class GetRoleByIdUseCase:
    """Caso de uso para buscar uma role pelo ID."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, role_id: UUID) -> RoleResponseDTO:
        """
        Busca uma role pelo ID.

        Args:
            role_id: UUID da role

        Returns:
            RoleResponseDTO: Dados da role encontrada

        Raises:
            RoleNotFoundException: Role não encontrada
        """
        entity_id = EntityId(role_id)
        role = await self._role_repository.find_by_id(entity_id)

        if role is None:
            raise RoleNotFoundException(f"Role com ID '{role_id}' não encontrada.")

        return to_role_response_dto(role)

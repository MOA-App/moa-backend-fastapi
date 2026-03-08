from app.modules.auth.application.dtos.role.role_inputs import RemovePermissionFromRoleDTO
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.shared.domain.value_objects.id_vo import EntityId


class RemovePermissionFromRoleUseCase:
    """Caso de uso para remover uma permissão de uma role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, dto: RemovePermissionFromRoleDTO) -> bool:
        """
        Remove a associação de uma permissão de uma role.

        Args:
            dto: IDs da role e da permissão

        Returns:
            bool: True se removida com sucesso

        Raises:
            RoleNotFoundException: Role não encontrada
            PermissionNotFoundException: Permissão não encontrada
            RoleNotAssignedException: Permissão não está associada à role
        """
        role_id = EntityId(dto.role_id)
        permission_id = EntityId(dto.permission_id)

        return await self._role_repository.remove_permission_from_role(role_id, permission_id)

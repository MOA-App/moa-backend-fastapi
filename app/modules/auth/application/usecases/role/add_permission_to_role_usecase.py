from app.modules.auth.application.dtos.role.role_inputs import AddPermissionToRoleDTO
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.shared.domain.value_objects.id_vo import EntityId


class AddPermissionToRoleUseCase:
    """Caso de uso para associar uma permissão a uma role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, dto: AddPermissionToRoleDTO) -> bool:
        """
        Associa uma permissão a uma role.

        Args:
            dto: IDs da role e da permissão

        Returns:
            bool: True se associada com sucesso

        Raises:
            RoleNotFoundException: Role não encontrada
            PermissionNotFoundException: Permissão não encontrada
            RoleAlreadyAssignedException: Permissão já associada à role
        """
        role_id = EntityId(dto.role_id)
        permission_id = EntityId(dto.permission_id)

        return await self._role_repository.add_permission_to_role(role_id, permission_id)

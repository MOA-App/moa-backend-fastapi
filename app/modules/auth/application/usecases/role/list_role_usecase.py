from app.modules.auth.application.dtos.role.role_outputs import RoleListResponseDTO
from app.modules.auth.application.mappers.role_mapper import to_role_response_dto
from app.modules.auth.domain.repositories.role_repository import RoleRepository


class ListRolesUseCase:
    """Caso de uso para listar todas as roles cadastradas."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self) -> RoleListResponseDTO:
        """
        Lista todas as roles.

        Returns:
            RoleListResponseDTO: Lista de roles com total
        """
        roles = await self._role_repository.list_all()
        role_dtos = [to_role_response_dto(r) for r in roles]

        return RoleListResponseDTO(roles=role_dtos, total=len(role_dtos))

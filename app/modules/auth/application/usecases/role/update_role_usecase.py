from app.modules.auth.application.dtos.role.role_inputs import UpdateRoleDTO
from app.modules.auth.application.dtos.role.role_outputs import RoleResponseDTO
from app.modules.auth.application.mappers.role_mapper import to_role_response_dto
from app.modules.auth.domain.exceptions.auth_exceptions import RoleAlreadyExistsException, RoleNotFoundException
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.modules.auth.domain.value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId


class UpdateRoleUseCase:
    """Caso de uso para atualização de uma role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, dto: UpdateRoleDTO) -> RoleResponseDTO:
        """
        Atualiza os dados de uma role.

        Args:
            dto: Dados para atualização

        Returns:
            RoleResponseDTO: Dados da role atualizada

        Raises:
            RoleNotFoundException: Role não encontrada
            RoleAlreadyExistsException: Novo nome já pertence a outra role
        """
        entity_id = EntityId(dto.role_id)
        role = await self._role_repository.find_by_id(entity_id)

        if role is None:
            raise RoleNotFoundException(f"Role com ID '{dto.role_id}' não encontrada.")

        if dto.name is not None:
            new_name = RoleName(dto.name)
            existing = await self._role_repository.find_by_name(new_name)
            if existing is not None and existing.id != entity_id:
                raise RoleAlreadyExistsException(f"Role '{dto.name}' já existe.")
            role.update_name(new_name)

        if dto.description is not None:
            role.update_description(dto.description)

        updated = await self._role_repository.update(role)
        return to_role_response_dto(updated)

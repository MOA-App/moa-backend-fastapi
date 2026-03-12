from app.modules.auth.application.dtos.role.role_inputs import CreateRoleDTO
from app.modules.auth.application.dtos.role.role_outputs import RoleResponseDTO
from app.modules.auth.application.mappers.role_mapper import to_role_response_dto
from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.exceptions.auth_exceptions import RoleAlreadyExistsException
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.modules.auth.domain.value_objects.role_name_vo import RoleName


class CreateRoleUseCase:
    """Caso de uso para criação de uma nova role."""

    def __init__(self, role_repository: RoleRepository) -> None:
        self._role_repository = role_repository

    async def execute(self, dto: CreateRoleDTO) -> RoleResponseDTO:
        """
        Executa a criação de uma role.

        Args:
            dto: Dados para criação da role

        Returns:
            RoleResponseDTO: Dados da role criada

        Raises:
            RoleAlreadyExistsException: Já existe uma role com o mesmo nome
        """
        name = RoleName(dto.name)

        already_exists = await self._role_repository.exists_by_name(name)
        if already_exists:
            raise RoleAlreadyExistsException(f"Role '{dto.name}' já existe.")

        role = Role.create(nome=name)

        created = await self._role_repository.create(role)

        return to_role_response_dto(created)

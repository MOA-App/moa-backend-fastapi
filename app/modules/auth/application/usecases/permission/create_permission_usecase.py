from app.modules.auth.application.dtos.permission.permission_inputs import CreatePermissionDTO
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.modules.auth.application.mappers.permission_mapper import PermissionMapper

from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.entities.permission_entity import Permission
from ....domain.value_objects.permission_name_vo import PermissionName
from ....domain.exceptions.auth_exceptions import (
    PermissionAlreadyExistsException,
)

class CreatePermissionUseCase:

    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def execute(self, dto: CreatePermissionDTO) -> PermissionResponseDTO:
        # 1. Criar VO (valida aqui)
        permission_name = PermissionName(dto.nome)

        # 2. Verificar existência
        if await self.permission_repository.exists_by_name(permission_name):
            raise PermissionAlreadyExistsException(permission_name.value)

        # 3. Criar entidade (VO, não string)
        permission = Permission.create(
            nome=permission_name,
            descricao=dto.descricao
        )

        # 4. Persistir
        created = await self.permission_repository.create(permission)

        # 5. Retornar
        return PermissionMapper.to_response_dto(created)

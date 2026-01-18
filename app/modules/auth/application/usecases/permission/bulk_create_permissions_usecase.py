from typing import List

from app.modules.auth.application.dtos.permission.permission_bulk import BulkCreatePermissionsDTO
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.modules.auth.application.dtos.permission.permission_queries import BulkCreatePermissionsResponseDTO
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidPermissionFormatException, RepositoryException

from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.entities.permission_entity import Permission
from ....domain.value_objects.permission_name_vo import PermissionName

class BulkCreatePermissionsUseCase:

    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def execute(
        self,
        dto: BulkCreatePermissionsDTO
    ) -> BulkCreatePermissionsResponseDTO:

        created: List[PermissionResponseDTO] = []
        skipped: List[str] = []
        errors: List[dict] = []

        for perm_dto in dto.permissions:
            try:
                permission_name = PermissionName(perm_dto.nome)

                if await self.permission_repository.find_by_name(permission_name):
                    skipped.append(permission_name.value)
                    continue

                permission = Permission.create(
                    nome=permission_name,
                    descricao=perm_dto.descricao
                )

                saved = await self.permission_repository.create(permission)

                created.append(
                    PermissionResponseDTO(
                        id=saved.id.value,
                        nome=saved.nome.value,
                        descricao=saved.descricao,
                        data_criacao=saved.data_criacao,
                        resource=str(saved.nome.get_resource()),
                        action=saved.nome.get_action()
                    )
                )

            except InvalidPermissionFormatException as e:
                errors.append({"nome": perm_dto.nome, "error": str(e)})

            except RepositoryException:
                errors.append({"nome": perm_dto.nome, "error": "Erro interno"})

        return BulkCreatePermissionsResponseDTO(
            created=created,
            skipped=skipped,
            errors=errors,
            total_created=len(created),
            total_skipped=len(skipped),
            total_errors=len(errors)
        )

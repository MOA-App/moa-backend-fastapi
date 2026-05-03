from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.modules.auth.application.mappers.permission_mapper import PermissionMapper
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidPermissionFormatException, PermissionNotFoundException
from app.modules.auth.domain.repositories.permission_repository import PermissionRepository
from app.modules.auth.domain.value_objects.permission_name_vo import PermissionName
from app.modules.auth.infrastructure.exceptions.repository_exception import RepositoryException


class GetPermissionByNameUseCase:
    """Caso de uso para obter permissão pelo nome"""

    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository

    async def execute(self, permission_name: str) -> PermissionResponseDTO:
        """
        Busca permissão por nome.

        Args:
            permission_name: Nome da permissão (ex: users.create)

        Returns:
            PermissionResponseDTO: Permissão encontrada

        Raises:
            PermissionNotFoundException: Permissão não encontrada
            InvalidPermissionFormatException: Nome da permissão inválido
        """
        try:
            # Validar formato do nome
            name_vo = PermissionName(permission_name)
        except ValueError as e:
            raise InvalidPermissionFormatException(str(e))

        try:
            permission = await self.permission_repository.find_by_name(name_vo)

            if not permission:
                raise PermissionNotFoundException(permission_name)

            return PermissionMapper.to_response_dto(permission)

        except PermissionNotFoundException:
            raise
        except InvalidPermissionFormatException:
            raise
        except Exception as e:
            raise RepositoryException(
                operation="buscar permissão por nome",
                details=str(e)
            )

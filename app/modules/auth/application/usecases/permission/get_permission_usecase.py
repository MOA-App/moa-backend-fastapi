from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.shared.domain.value_objects.id_vo import EntityId
from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.exceptions.auth_exceptions import (
    PermissionNotFoundException,
    RepositoryException
)


class GetPermissionUseCase:
    """Caso de uso para obter permissão por ID"""
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(self, permission_id: str) -> PermissionResponseDTO:
        """
        Busca permissão por ID.
        
        Args:
            permission_id: UUID da permissão
            
        Returns:
            PermissionResponseDTO: Permissão encontrada
            
        Raises:
            PermissionNotFoundException: Permissão não encontrada
        """
        try:
            entity_id = EntityId.from_string(permission_id)
        except ValueError as e:
            raise PermissionNotFoundException(permission_id)
        
        try:
            permission = await self.permission_repository.find_by_id(entity_id)
            
            if not permission:
                raise PermissionNotFoundException(permission_id)
            
            return PermissionResponseDTO(
                id=permission.id.value,
                nome=permission.nome.value,
                descricao=permission.descricao,
                data_criacao=permission.data_criacao,
                resource=permission.get_resource(),
                action=permission.get_action()
            )
            
        except PermissionNotFoundException:
            raise
        except Exception as e:
            raise RepositoryException(
                operation="buscar permissão",
                details=str(e)
            )

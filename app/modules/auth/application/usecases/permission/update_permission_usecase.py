from app.modules.auth.application.dtos.permission.permission_inputs import UpdatePermissionDTO
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.modules.auth.application.mappers.permission_mapper import PermissionMapper
from app.shared.domain.value_objects.id_vo import EntityId
from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.exceptions.auth_exceptions import (
    PermissionNotFoundException,
    RepositoryException
)


class UpdatePermissionUseCase:
    """
    Caso de uso para atualizar permissão.
    
    Nota: Apenas a descrição pode ser atualizada.
    Para mudar o nome, deve criar nova permissão.
    """
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(
        self,
        permission_id: str,
        dto: UpdatePermissionDTO
    ) -> PermissionResponseDTO:
        """
        Atualiza descrição da permissão.
        
        Args:
            permission_id: UUID da permissão
            dto: Dados a atualizar
            
        Returns:
            PermissionResponseDTO: Permissão atualizada
            
        Raises:
            PermissionNotFoundException: Permissão não encontrada
        """
        try:
            entity_id = EntityId.from_string(permission_id)
        except ValueError:
            raise PermissionNotFoundException(permission_id)
        
        try:
            # Buscar permissão
            permission = await self.permission_repository.find_by_id(entity_id)
            
            if not permission:
                raise PermissionNotFoundException(permission_id)
            
            # Atualizar descrição (retorna nova instância por ser imutável)
            updated_permission = permission.update_description(dto.descricao)
            
            # Persistir
            saved = await self.permission_repository.update(updated_permission)
            
            return PermissionMapper.to_response_dto(saved)
            
        except PermissionNotFoundException:
            raise
        except Exception as e:
            raise RepositoryException(
                operation="atualizar permissão",
                details=str(e)
            )

from typing import List

from app.modules.auth.application.dtos.permission.permission_outputs import ResourceActionsDTO

from ....domain.repositories.permission_repository import PermissionRepository


class ListResourcesUseCase:
    """Lista todos os recursos que possuem permissões"""
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(self) -> List[str]:
        """
        Retorna lista de recursos únicos.
        
        Returns:
            List[str]: Lista de recursos (ex: ['users', 'posts', 'admin'])
        """
        return await self.permission_repository.list_resources()
    
    async def get_resource_actions(self, resource: str) -> ResourceActionsDTO:
        """
        Retorna ações disponíveis para um recurso.
        
        Args:
            resource: Nome do recurso
            
        Returns:
            ResourceActionsDTO: Recurso e suas ações
        """
        actions = await self.permission_repository.list_actions(resource)
        
        return ResourceActionsDTO(
            resource=resource,
            actions=actions
        )

from typing import List, Optional

from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.exceptions.auth_exceptions import RepositoryException

from ..dtos.permission_dto import (
    PermissionResponseDTO,
    ListPermissionsQueryDTO,
    PermissionsByResourceDTO,
    PermissionSummaryDTO
)


class ListPermissionsUseCase:
    """
    Caso de uso para listar permissões.
    
    Suporta:
    - Listagem completa
    - Filtro por recurso
    - Busca por nome/descrição
    - Paginação
    """
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(
        self,
        query: Optional[ListPermissionsQueryDTO] = None
    ) -> List[PermissionResponseDTO]:
        """
        Lista permissões com filtros opcionais.
        
        Args:
            query: Parâmetros de busca e paginação
            
        Returns:
            List[PermissionResponseDTO]: Lista de permissões
        """
        try:
            # Se filtro por recurso
            if query and query.resource:
                permissions = await self.permission_repository.list_by_resource(
                    query.resource
                )
            else:
                # Listar todas
                permissions = await self.permission_repository.list_all()
            
            # Aplicar busca textual (se informada)
            if query and query.search:
                search_lower = query.search.lower()
                permissions = [
                    p for p in permissions
                    if search_lower in p.nome.value.lower() or
                       (p.descricao and search_lower in p.descricao.lower())
                ]
            
            # Aplicar paginação (se informada)
            if query:
                start = (query.page - 1) * query.page_size
                end = start + query.page_size
                permissions = permissions[start:end]
            
            # Converter para DTOs
            return [self._to_response_dto(p) for p in permissions]
            
        except Exception as e:
            raise RepositoryException(
                operation="listar permissões",
                details=str(e)
            )
    
    async def list_by_resource(self, resource: str) -> List[PermissionResponseDTO]:
        """Lista permissões de um recurso específico"""
        try:
            permissions = await self.permission_repository.list_by_resource(resource)
            return [self._to_response_dto(p) for p in permissions]
        except Exception as e:
            raise RepositoryException(
                operation=f"listar permissões do recurso {resource}",
                details=str(e)
            )
    
    async def group_by_resource(self) -> List[PermissionsByResourceDTO]:
        """Agrupa permissões por recurso"""
        try:
            # Obter todas as permissões
            all_permissions = await self.permission_repository.list_all()
            
            # Agrupar por recurso
            resources_dict = {}
            for permission in all_permissions:
                resource = permission.get_resource()
                
                if resource not in resources_dict:
                    resources_dict[resource] = []
                
                resources_dict[resource].append(permission)
            
            # Converter para DTOs
            result = []
            for resource, permissions in sorted(resources_dict.items()):
                result.append(
                    PermissionsByResourceDTO(
                        resource=resource,
                        permissions=[
                            PermissionSummaryDTO(
                                id=p.id.value,
                                nome=p.nome.value,
                                descricao=p.descricao
                            )
                            for p in permissions
                        ],
                        total=len(permissions)
                    )
                )
            
            return result
            
        except Exception as e:
            raise RepositoryException(
                operation="agrupar permissões por recurso",
                details=str(e)
            )
    
    def _to_response_dto(self, permission: Permission) -> PermissionResponseDTO:
        """Converte Entity para DTO"""
        return PermissionResponseDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao,
            data_criacao=permission.data_criacao,
            resource=permission.get_resource(),
            action=permission.get_action()
        )

import math
from typing import List, Optional

from app.modules.auth.application.dtos.permission.paginated_result import PaginatedResult
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO, PermissionSummaryDTO, ResourceActionsDTO
from app.modules.auth.application.dtos.permission.permission_queries import ListPermissionsQueryDTO
from app.modules.auth.application.mappers.permission_mapper import PermissionMapper
from app.modules.auth.domain.entities.permission_entity import Permission
from app.modules.auth.infrastructure.exceptions.repository_exception import RepositoryException

from ....domain.repositories.permission_repository import PermissionRepository



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
    ) -> PaginatedResult[PermissionSummaryDTO]:
        """
        Lista permissões com filtros opcionais.

        """
        try:
            permissions = await self.permission_repository.list_all()

            total = len(permissions)

            if not query:
                query = ListPermissionsQueryDTO()

            start = (query.page - 1) * query.page_size
            end = start + query.page_size
            page_items = permissions[start:end]

            return PaginatedResult(
                items=[
                    PermissionMapper.to_summary_dto(p)
                    for p in page_items
                ],
                total=total,
                page=query.page,
                page_size=query.page_size,
                total_pages=math.ceil(total / query.page_size)
            )
                    
        except Exception as e:
            raise RepositoryException(
                operation="listar permissões",
                details=str(e)
            )
    
    async def list_by_resource(self, resource: str) -> List[PermissionSummaryDTO]:
        """Lista permissões de um recurso específico"""
        try:
            permissions = await self.permission_repository.list_by_resource(resource)
            return [
                PermissionMapper.to_summary_dto(permission)
                for permission in permissions
            ]
        except Exception as e:
            raise RepositoryException(
                operation=f"listar permissões do recurso {resource}",
                details=str(e)
            )
    
    async def group_by_resource(self) -> List[ResourceActionsDTO]:
        try:
            permissions = await self.permission_repository.list_all()
            return PermissionMapper.group_actions_by_resource(permissions)

        except Exception as e:
            raise RepositoryException(
                operation="agrupar ações por recurso",
                details=str(e)
            )

    
    def _to_response_dto(self, permission: Permission) -> PermissionResponseDTO:
        """Converte Entity para DTO"""
        return PermissionResponseDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao,
            data_criacao=permission.data_criacao,
            resource=permission.resource(),
            action=permission.action()
        )

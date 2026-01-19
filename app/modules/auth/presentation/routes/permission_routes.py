from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List
from uuid import UUID

from app.modules.auth.application.dtos.permission.permission_bulk import BulkCreatePermissionsDTO
from app.modules.auth.application.dtos.permission.permission_inputs import CreatePermissionDTO, UpdatePermissionDTO
from app.modules.auth.application.usecases.permission.bulk_create_permissions_usecase import BulkCreatePermissionsUseCase
from app.modules.auth.application.usecases.permission.create_permission_usecase import CreatePermissionUseCase
from app.modules.auth.application.usecases.permission.delete_permission_usecase import DeletePermissionUseCase
from app.modules.auth.application.usecases.permission.get_permission_usecase import GetPermissionUseCase
from app.modules.auth.application.usecases.permission.list_permissions_usecase import ListPermissionsUseCase
from app.modules.auth.application.usecases.permission.list_resources_usecase import ListResourcesUseCase
from app.modules.auth.application.usecases.permission.update_permission_usecase import UpdatePermissionUseCase
from app.modules.auth.presentation.schemas.permission.bulk_create_request_schema import BulkCreatePermissionsRequest
from app.modules.auth.presentation.schemas.permission.bulk_create_response_schema import BulkCreatePermissionsResponse
from app.modules.auth.presentation.schemas.permission.create_permission_schema import CreatePermissionRequest
from app.modules.auth.presentation.schemas.permission.error_response_schema import ErrorResponse
from app.modules.auth.presentation.schemas.permission.list_permissions_schema import ListPermissionsQuery
from app.modules.auth.presentation.schemas.permission.message_response_schema import MessageResponse
from app.modules.auth.presentation.schemas.permission.permission_by_resource_response import PermissionByResourceResponse
from app.modules.auth.presentation.schemas.permission.permission_list_response import PermissionListMeta, PermissionListResponse
from app.modules.auth.presentation.schemas.permission.permission_response import PermissionResponse
from app.modules.auth.presentation.schemas.permission.permission_stats_schema import PermissionStats
from app.modules.auth.presentation.schemas.permission.resource_actions_schema import ResourceActions
from app.modules.auth.presentation.schemas.permission.update_permission_schema import UpdatePermissionRequest


from ..dependencies.auth_deps import (
    get_bulk_create_permissions_usecase,
    get_create_permission_usecase,
    get_delete_permission_usecase,
    get_list_permissions_usecase,
    get_list_resources_usecase,
    get_permission_usecase,
    get_update_permission_usecase,
    require_permission
)

from ...domain.exceptions.auth_exceptions import (
    DomainValidationException,
    PermissionAlreadyExistsException,
    PermissionNotFoundException
)

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/permissions", tags=["Permissions"])


# ============================================================================
# CRUD ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=PermissionResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova permissão",
    description="Cria uma nova permissão no sistema. Requer permissão: permissions.create",
    responses={
        201: {"description": "Permissão criada com sucesso"},
        400: {"model": ErrorResponse},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.create"},
        422: {"description": "Erro de validação"}
    }
)
async def create_permission(
    body: CreatePermissionRequest,
    usecase: CreatePermissionUseCase = Depends(get_create_permission_usecase),
    _: None = Depends(require_permission("permissions.create"))
) -> PermissionResponse:
    """
    Cria uma nova permissão.
    
    **Formato do nome**: resource.action (ex: users.create, posts.delete)
    
    **Validações**:
    - Nome único
    - Formato correto (2-5 níveis)
    - Apenas lowercase, números e underscore
    
    **Exemplo**:
    ```json
    {
        "nome": "users.create",
        "descricao": "Permite criar novos usuários"
    }
    ```
    """
    try:
        #logger.info(f"Creating permission: {dto.nome} by user {current_user.id}")
        dto = CreatePermissionDTO(
            nome=body.nome,
            descricao=body.descricao
        )

        permission = await usecase.execute(dto)
        logger.info(f"Permission created successfully: {permission.id}")
        return permission
        
    except PermissionAlreadyExistsException as e:
        logger.warning(f"Permission already exists: {dto.nome}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "permission_exists", "message": str(e)}
        )
    except DomainValidationException as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "validation_error", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error creating permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao criar permissão"}
        )


@router.get(
    "",
    response_model=PermissionListResponse,
    summary="Listar permissões",
    description="Lista permissões com filtros opcionais. Requer: permissions.read",
)
async def list_permissions(
    query: ListPermissionsQuery = Depends(),
    usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> PermissionListResponse:
    try:
        result = await usecase.execute(query)

        return PermissionListResponse(
            data=result.items,
            meta=PermissionListMeta(
                total=result.total,
                page=query.page,
                limit=query.limit,
                total_pages=result.total_pages
            )
        )

    except Exception as e:
        logger.error(f"Error listing permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=500,
            detail={"error": "internal_error", "message": "Erro ao listar permissões"}
        )


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Obter permissão por ID",
    description="Retorna detalhes de uma permissão específica. Requer: permissions.read",
    responses={
        200: {"description": "Permissão encontrada"},
        404: {"description": "Permissão não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.read"}
    }
)
async def get_permission(
    permission_id: UUID,
    usecase: GetPermissionUseCase = Depends(get_permission_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> PermissionResponse:
    """
    Retorna detalhes de uma permissão específica.
    
    **Path Parameter**:
    - `permission_id`: UUID da permissão
    """
    try:
        logger.info(f"Getting permission: {permission_id}")
        permission = await usecase.execute(str(permission_id))
        return permission
        
    except PermissionNotFoundException as e:
        logger.warning(f"Permission not found: {permission_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "permission_not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error getting permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao buscar permissão"}
        )


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Atualizar permissão",
    description="Atualiza descrição de uma permissão. Requer: permissions.update",
    responses={
        200: {"description": "Permissão atualizada"},
        404: {"description": "Permissão não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.update"}
    }
)
async def update_permission(
    permission_id: UUID,
    body: UpdatePermissionRequest,
    usecase: UpdatePermissionUseCase = Depends(get_update_permission_usecase),
    _: None = Depends(require_permission("permissions.update"))
) -> PermissionResponse:
    """
    Atualiza descrição de uma permissão.
    
    **Nota**: O nome da permissão não pode ser alterado.
    Para isso, crie uma nova permissão.
    
    **Exemplo**:
    ```json
    {
        "descricao": "Nova descrição da permissão"
    }
    ```
    """
    try:
        logger.info(f"Updating permission: {permission_id}")
        dto = UpdatePermissionDTO(descricao=body.descricao)
        permission = await usecase.execute(str(permission_id), dto)
        logger.info(f"Permission updated successfully: {permission_id}")
        return permission
        
    except PermissionNotFoundException as e:
        logger.warning(f"Permission not found: {permission_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "permission_not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error updating permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao atualizar permissão"}
        )


@router.delete(
    "/{permission_id}",
    response_model=MessageResponse,
    summary="Deletar permissão",
    description="Remove uma permissão do sistema. Requer: permissions.delete",
    responses={
        200: {"description": "Permissão deletada"},
        404: {"description": "Permissão não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.delete"}
    }
)
async def delete_permission(
    permission_id: UUID,
    usecase: DeletePermissionUseCase = Depends(get_delete_permission_usecase),
    _: None = Depends(require_permission("permissions.delete"))
) -> MessageResponse:
    """
    Deleta uma permissão do sistema.
    
    **Atenção**: Esta ação é irreversível e removerá a permissão
    de todas as roles que a possuem.
    """
    try:
        logger.info(f"Deleting permission: {permission_id}")
        await usecase.execute(str(permission_id))
        logger.info(f"Permission deleted successfully: {permission_id}")
        
        return MessageResponse(
            message=f"Permissão {permission_id} deletada com sucesso"
        )
        
    except PermissionNotFoundException as e:
        logger.warning(f"Permission not found: {permission_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "permission_not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error deleting permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao deletar permissão"}
        )


# ============================================================================
# BULK OPERATIONS
# ============================================================================

@router.post(
    "/bulk",
    response_model=BulkCreatePermissionsResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar múltiplas permissões",
    description="Cria várias permissões de uma vez. Requer: permissions.create",
    responses={
        201: {"description": "Permissões criadas (com relatório)"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.create"}
    }
)
async def bulk_create_permissions(
    body: BulkCreatePermissionsRequest,
    usecase: BulkCreatePermissionsUseCase = Depends(get_bulk_create_permissions_usecase),
    _: None = Depends(require_permission("permissions.create"))
) -> BulkCreatePermissionsResponse:
    """
    Cria múltiplas permissões em lote.
    
    **Comportamento**:
    - Permissões existentes são ignoradas
    - Permissões inválidas são reportadas como erro
    - Operação continua mesmo com erros parciais
    
    **Exemplo**:
    ```json
    {
        "permissions": [
            {"nome": "users.create", "descricao": "Criar usuários"},
            {"nome": "users.read", "descricao": "Ler usuários"},
            {"nome": "users.update", "descricao": "Atualizar usuários"}
        ]
    }
    ```
    
    **Resposta**:
    ```json
    {
        "created": [...],
        "skipped": ["users.read"],
        "errors": [],
        "total_created": 2,
        "total_skipped": 1,
        "total_errors": 0
    }
    ```
    """
    try:
        dto = BulkCreatePermissionsDTO(
            permissions=[
                CreatePermissionDTO(
                    nome=p.nome,
                    descricao=p.descricao
                )
                for p in body.permissions
            ]
        )

        logger.info(f"Bulk creating {len(dto.permissions)} permissions")
        result = await usecase.execute(dto)
        logger.info(
            f"Bulk create result: {result.total_created} created, "
            f"{result.total_skipped} skipped, {result.total_errors} errors"
        )
        return result
        
    except Exception as e:
        logger.error(f"Error in bulk create: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao criar permissões em lote"}
        )


# ============================================================================
# RESOURCE & ACTIONS ENDPOINTS
# ============================================================================

@router.get(
    "/resources/list",
    response_model=List[str],
    summary="Listar recursos",
    description="Lista todos os recursos únicos. Requer: permissions.read",
    responses={
        200: {"description": "Lista de recursos"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão"}
    }
)
async def list_resources(
    usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> List[str]:
    """
    Lista todos os recursos que possuem permissões cadastradas.
    
    **Retorna**: Lista de recursos únicos (ex: ['users', 'posts', 'admin'])
    """
    try:
        logger.info("Listing resources")
        resources = await usecase.execute()
        logger.info(f"Found {len(resources)} resources")
        return resources
        
    except Exception as e:
        logger.error(f"Error listing resources: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao listar recursos"}
        )


@router.get(
    "/resources/{resource}/actions",
    response_model=ResourceActions,
    summary="Listar ações de um recurso",
    description="Lista ações disponíveis para um recurso. Requer: permissions.read"
)
async def get_resource_actions(
    resource: str,
    usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> ResourceActions:
    """
    Lista todas as ações disponíveis para um recurso específico.
    
    **Path Parameter**:
    - `resource`: Nome do recurso (ex: users, posts)
    
    **Retorna**: Recurso e lista de ações
    
    **Exemplo**: `/permissions/resources/users/actions`
    
    **Resposta**:
    ```json
    {
        "resource": "users",
        "actions": ["create", "read", "update", "delete"]
    }
    ```
    """
    try:
        logger.info(f"Getting actions for resource: {resource}")
        result = await usecase.get_resource_actions(resource)
        return result
        
    except Exception as e:
        logger.error(f"Error getting resource actions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao listar ações"}
        )


@router.get(
    "/grouped-by-resource",
    response_model=List[PermissionByResourceResponse],
    summary="Permissões agrupadas por recurso",
    description="Retorna permissões agrupadas por recurso. Requer: permissions.read"
)
async def get_permissions_grouped_by_resource(
    usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> List[PermissionByResourceResponse]:
    """
    Retorna permissões agrupadas por recurso.
    
    **Resposta**:
    ```json
    [
        {
            "resource": "users",
            "permissions": [...],
            "total": 5
        },
        {
            "resource": "posts",
            "permissions": [...],
            "total": 4
        }
    ]
    ```
    """
    try:
        logger.info("Getting permissions grouped by resource")
        groups = await usecase.group_by_resource()
        return groups
        
    except Exception as e:
        logger.error(f"Error grouping permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao agrupar permissões"}
        )

# ============================================================================
# STATISTICS & REPORTS
# ============================================================================

@router.get(
    "/stats",
    response_model=PermissionStats,
    summary="Estatísticas de permissões",
    description="Retorna estatísticas sobre permissões. Requer: permissions.read",
    responses={
        200: {"description": "Estatísticas"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão"}
    }
)
async def get_permission_stats(
    list_usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
    resources_usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> PermissionStats:
    """
    Retorna estatísticas gerais sobre permissões.
    
    **Retorna**:
    - Total de permissões
    - Total de recursos
    - Lista de recursos
    - Top 10 permissões mais usadas
    """
    try:
        logger.info("Getting permission statistics")
        
        # Obter todas as permissões
        all_permissions = await list_usecase.execute()
        
        # Obter recursos únicos
        resources = await resources_usecase.execute()
        
        # TODO: Implementar "most_used_permissions" quando tiver o método no repository
        most_used = []
        
        stats = PermissionStats(
            total_permissions=len(all_permissions),
            total_resources=len(resources),
            resources=resources,
            most_used_permissions=most_used
        )
        
        logger.info(f"Stats: {stats.total_permissions} permissions, {stats.total_resources} resources")
        return stats
        
    except Exception as e:
        logger.error(f"Error getting stats: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao obter estatísticas"}
        )

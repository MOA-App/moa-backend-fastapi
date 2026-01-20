from fastapi import APIRouter, Depends, status
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
from app.modules.auth.presentation.dependencies.permissions import require_permission
from app.modules.auth.presentation.schemas.permission.bulk_create_request_schema import BulkCreatePermissionsRequest
from app.modules.auth.presentation.schemas.permission.bulk_create_response_schema import BulkCreatePermissionsResponse
from app.modules.auth.presentation.schemas.permission.create_permission_schema import CreatePermissionRequest
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
)

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
    dto = CreatePermissionDTO(
        nome=body.nome,
        descricao=body.descricao
    )

    permission = await usecase.execute(dto)
    return permission


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

@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Obter permissão por ID",
    description="Retorna detalhes de uma permissão específica. Requer: permissions.read",
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
    permission = await usecase.execute(str(permission_id))
    return permission


@router.put(
    "/{permission_id}",
    response_model=PermissionResponse,
    summary="Atualizar permissão",
    description="Atualiza descrição de uma permissão. Requer: permissions.update",
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
    dto = UpdatePermissionDTO(descricao=body.descricao)
    permission = await usecase.execute(str(permission_id), dto)
    return permission


@router.delete(
    "/{permission_id}",
    response_model=MessageResponse,
    summary="Deletar permissão",
    description="Remove uma permissão do sistema. Requer: permissions.delete",
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
    await usecase.execute(str(permission_id))
    
    return MessageResponse(
        message=f"Permissão {permission_id} deletada com sucesso"
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
    dto = BulkCreatePermissionsDTO(
        permissions=[
            CreatePermissionDTO(
                nome=p.nome,
                descricao=p.descricao
            )
            for p in body.permissions
        ]
    )
    result = await usecase.execute(dto)
    return result

# ============================================================================
# RESOURCE & ACTIONS ENDPOINTS
# ============================================================================

@router.get(
    "/resources/list",
    response_model=List[str],
    summary="Listar recursos",
    description="Lista todos os recursos únicos. Requer: permissions.read",
)
async def list_resources(
    usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
    _: None = Depends(require_permission("permissions.read"))
) -> List[str]:
    """
    Lista todos os recursos que possuem permissões cadastradas.
    
    **Retorna**: Lista de recursos únicos (ex: ['users', 'posts', 'admin'])
    """
    resources = await usecase.execute()
    return resources


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
    result = await usecase.get_resource_actions(resource)
    return result

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
    groups = await usecase.group_by_resource()
    return groups


# ============================================================================
# STATISTICS & REPORTS
# ============================================================================

@router.get(
    "/stats",
    response_model=PermissionStats,
    summary="Estatísticas de permissões",
    description="Retorna estatísticas sobre permissões. Requer: permissions.read",
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
    return stats

from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import List, Optional
from uuid import UUID

from ...application.dtos.permission_dto import (
    CreatePermissionDTO,
    UpdatePermissionDTO,
    PermissionResponseDTO,
    PermissionSummaryDTO,
    PermissionDetailDTO,
    PermissionsByResourceDTO,
    ResourceActionsDTO,
    PermissionStatsDTO,
    BulkCreatePermissionsDTO,
    BulkCreatePermissionsResponseDTO,
    AssignPermissionToRoleDTO,
    RevokePermissionFromRoleDTO,
    ListPermissionsQueryDTO
)
from ...application.dtos.response_dto import MessageResponseDTO, ErrorResponseDTO
from ...application.dtos.user_response_dto import UserResponseDTO

from ...application.usecases.create_permission_usecase import CreatePermissionUseCase
from ...application.usecases.get_permission_usecase import GetPermissionUseCase
from ...application.usecases.list_permissions_usecase import ListPermissionsUseCase
from ...application.usecases.update_permission_usecase import UpdatePermissionUseCase
from ...application.usecases.delete_permission_usecase import DeletePermissionUseCase
from ...application.usecases.bulk_create_permissions_usecase import BulkCreatePermissionsUseCase
from ...application.usecases.list_resources_usecase import ListResourcesUseCase
from ...application.usecases.assign_permission_to_role_usecase import AssignPermissionToRoleUseCase
from ...application.usecases.revoke_permission_from_role_usecase import RevokePermissionFromRoleUseCase
from ...application.usecases.get_role_permissions_usecase import GetRolePermissionsUseCase
from ...application.usecases.check_user_permission_usecase import CheckUserPermissionUseCase
from ...application.usecases.get_user_permissions_usecase import GetUserPermissionsUseCase

from ..dependencies.permission_deps import (
    get_create_permission_usecase,
    get_get_permission_usecase,
    get_list_permissions_usecase,
    get_update_permission_usecase,
    get_delete_permission_usecase,
    get_bulk_create_permissions_usecase,
    get_list_resources_usecase,
    get_assign_permission_to_role_usecase,
    get_revoke_permission_from_role_usecase,
    get_get_role_permissions_usecase,
    get_check_user_permission_usecase,
    get_get_user_permissions_usecase
)

from ..dependencies.auth_deps import (
    get_current_user,
    require_permission,
    require_any_permission
)

from ...domain.exceptions.auth_exceptions import (
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
    RoleNotFoundException,
    DomainValidationException,
    RepositoryException
)

import logging

logger = logging.getLogger(__name__)


router = APIRouter(prefix="/permissions", tags=["Permissions"])


# ============================================================================
# CRUD ENDPOINTS
# ============================================================================

@router.post(
    "",
    response_model=PermissionResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar nova permissão",
    description="Cria uma nova permissão no sistema. Requer permissão: permissions.create",
    responses={
        201: {"description": "Permissão criada com sucesso"},
        400: {
            "description": "Dados inválidos ou permissão já existe",
            "model": ErrorResponseDTO
        },
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.create"},
        422: {"description": "Erro de validação"}
    }
)
async def create_permission(
    dto: CreatePermissionDTO,
    usecase: CreatePermissionUseCase = Depends(get_create_permission_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.create"))
) -> PermissionResponseDTO:
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
        logger.info(f"Creating permission: {dto.nome} by user {current_user.id}")
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
    response_model=List[PermissionResponseDTO],
    summary="Listar permissões",
    description="Lista permissões com filtros opcionais. Requer: permissions.read",
    responses={
        200: {"description": "Lista de permissões"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.read"}
    }
)
async def list_permissions(
    resource: Optional[str] = Query(
        None,
        description="Filtrar por recurso específico",
        example="users"
    ),
    search: Optional[str] = Query(
        None,
        min_length=1,
        max_length=100,
        description="Buscar em nome ou descrição"
    ),
    page: int = Query(1, ge=1, description="Número da página"),
    page_size: int = Query(20, ge=1, le=100, description="Itens por página"),
    usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> List[PermissionResponseDTO]:
    """
    Lista permissões com filtros e paginação.
    
    **Filtros disponíveis**:
    - `resource`: Filtrar por recurso (ex: users, posts)
    - `search`: Buscar em nome ou descrição
    - `page`: Número da página (padrão: 1)
    - `page_size`: Itens por página (padrão: 20, max: 100)
    
    **Exemplo**: `/permissions?resource=users&page=1&page_size=10`
    """
    try:
        query = ListPermissionsQueryDTO(
            resource=resource,
            search=search,
            page=page,
            page_size=page_size
        )
        
        logger.info(f"Listing permissions with filters: resource={resource}, search={search}")
        permissions = await usecase.execute(query)
        logger.info(f"Found {len(permissions)} permissions")
        
        return permissions
        
    except Exception as e:
        logger.error(f"Error listing permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao listar permissões"}
        )


@router.get(
    "/{permission_id}",
    response_model=PermissionResponseDTO,
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
    usecase: GetPermissionUseCase = Depends(get_get_permission_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> PermissionResponseDTO:
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
    response_model=PermissionResponseDTO,
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
    dto: UpdatePermissionDTO,
    usecase: UpdatePermissionUseCase = Depends(get_update_permission_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.update"))
) -> PermissionResponseDTO:
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
    response_model=MessageResponseDTO,
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
    current_user: UserResponseDTO = Depends(require_permission("permissions.delete"))
) -> MessageResponseDTO:
    """
    Deleta uma permissão do sistema.
    
    **Atenção**: Esta ação é irreversível e removerá a permissão
    de todas as roles que a possuem.
    """
    try:
        logger.info(f"Deleting permission: {permission_id}")
        await usecase.execute(str(permission_id))
        logger.info(f"Permission deleted successfully: {permission_id}")
        
        return MessageResponseDTO(
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
    response_model=BulkCreatePermissionsResponseDTO,
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
    dto: BulkCreatePermissionsDTO,
    usecase: BulkCreatePermissionsUseCase = Depends(get_bulk_create_permissions_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.create"))
) -> BulkCreatePermissionsResponseDTO:
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
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
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
    response_model=ResourceActionsDTO,
    summary="Listar ações de um recurso",
    description="Lista ações disponíveis para um recurso. Requer: permissions.read"
)
async def get_resource_actions(
    resource: str,
    usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> ResourceActionsDTO:
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
    response_model=List[PermissionsByResourceDTO],
    summary="Permissões agrupadas por recurso",
    description="Retorna permissões agrupadas por recurso. Requer: permissions.read"
)
async def get_permissions_grouped_by_resource(
    usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> List[PermissionsByResourceDTO]:
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
# ROLE PERMISSION ENDPOINTS
# ============================================================================

@router.post(
    "/assign-to-role",
    response_model=MessageResponseDTO,
    summary="Atribuir permissão a role",
    description="Atribui uma permissão a uma role. Requer: permissions.assign",
    responses={
        200: {"description": "Permissão atribuída"},
        404: {"description": "Permissão ou role não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.assign"}
    }
)
async def assign_permission_to_role(
    dto: AssignPermissionToRoleDTO,
    usecase: AssignPermissionToRoleUseCase = Depends(get_assign_permission_to_role_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.assign"))
) -> MessageResponseDTO:
    """
    Atribui uma permissão a uma role.
    
    **Exemplo**:
    ```json
    {
        "role_id": "123e4567-e89b-12d3-a456-426614174000",
        "permission_id": "987fcdeb-51a2-43f7-9876-543210fedcba"
    }
    ```
    """
    try:
        logger.info(f"Assigning permission {dto.permission_id} to role {dto.role_id}")
        result = await usecase.execute(dto)
        logger.info("Permission assigned successfully")
        return result
        
    except (PermissionNotFoundException, RoleNotFoundException) as e:
        logger.warning(f"Not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error assigning permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao atribuir permissão"}
        )


@router.post(
    "/revoke-from-role",
    response_model=MessageResponseDTO,
    summary="Remover permissão de role",
    description="Remove uma permissão de uma role. Requer: permissions.revoke",
    responses={
        200: {"description": "Permissão removida"},
        404: {"description": "Permissão ou role não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão: permissions.revoke"}
    }
)
async def revoke_permission_from_role(
    dto: RevokePermissionFromRoleDTO,
    usecase: RevokePermissionFromRoleUseCase = Depends(get_revoke_permission_from_role_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.revoke"))
) -> MessageResponseDTO:
    """
    Remove uma permissão de uma role.
    
    **Exemplo**:
    ```json
    {
        "role_id": "123e4567-e89b-12d3-a456-426614174000",
        "permission_id": "987fcdeb-51a2-43f7-9876-543210fedcba"
    }
    ```
    """
    try:
        logger.info(f"Revoking permission {dto.permission_id} from role {dto.role_id}")
        result = await usecase.execute(dto)
        logger.info("Permission revoked successfully")
        return result
        
    except (PermissionNotFoundException, RoleNotFoundException) as e:
        logger.warning(f"Not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error revoking permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao remover permissão"}
        )


@router.get(
    "/role/{role_id}",
    response_model=List[PermissionResponseDTO],
    summary="Obter permissões de uma role",
    description="Lista permissões de uma role específica. Requer: permissions.read",
    responses={
        200: {"description": "Lista de permissões da role"},
        404: {"description": "Role não encontrada"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão"}
    }
)
async def get_role_permissions(
    role_id: UUID,
    usecase: GetRolePermissionsUseCase = Depends(get_get_role_permissions_usecase),
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> List[PermissionResponseDTO]:
    """
    Lista todas as permissões de uma role específica.
    
    **Path Parameter**:
    - `role_id`: UUID da role
    """
    try:
        logger.info(f"Getting permissions for role: {role_id}")
        permissions = await usecase.execute(str(role_id))
        logger.info(f"Found {len(permissions)} permissions for role")
        return permissions
        
    except RoleNotFoundException as e:
        logger.warning(f"Role not found: {role_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "role_not_found", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Error getting role permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao buscar permissões"}
        )


# ============================================================================
# USER PERMISSION ENDPOINTS
# ============================================================================

@router.get(
    "/user/{user_id}",
    response_model=List[PermissionResponseDTO],
    summary="Obter permissões de um usuário",
    description="Lista todas as permissões de um usuário (via roles). Requer: permissions.read",
    responses={
        200: {"description": "Lista de permissões do usuário"},
        404: {"description": "Usuário não encontrado"},
        401: {"description": "Não autenticado"},
        403: {"description": "Sem permissão"}
    }
)
async def get_user_permissions(
    user_id: UUID,
    usecase: GetUserPermissionsUseCase = Depends(get_get_user_permissions_usecase),
    current_user: UserResponseDTO = Depends(
        require_any_permission("permissions.read", "users.read")
    )
) -> List[PermissionResponseDTO]:
    """
    Lista todas as permissões de um usuário (agregadas de todas as suas roles).
    
    **Path Parameter**:
    - `user_id`: UUID do usuário
    
    **Retorna**: Lista de permissões únicas (sem duplicatas)
    """
    try:
        logger.info(f"Getting permissions for user: {user_id}")
        permissions = await usecase.execute(str(user_id))
        logger.info(f"User has {len(permissions)} permissions")
        return permissions
        
    except Exception as e:
        logger.error(f"Error getting user permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao buscar permissões"}
        )


@router.get(
    "/user/{user_id}/check/{permission_name}",
    response_model=dict,
    summary="Verificar se usuário tem permissão",
    description="Verifica se um usuário possui uma permissão específica",
    responses={
        200: {"description": "Resultado da verificação"},
        404: {"description": "Usuário não encontrado"},
        401: {"description": "Não autenticado"}
    }
)
async def check_user_permission(
    user_id: UUID,
    permission_name: str,
    usecase: CheckUserPermissionUseCase = Depends(get_check_user_permission_usecase),
    current_user: UserResponseDTO = Depends(get_current_user)
) -> dict:
    """
    Verifica se um usuário possui uma permissão específica.
    
    **Path Parameters**:
    - `user_id`: UUID do usuário
    - `permission_name`: Nome da permissão (ex: users.create)
    
    **Resposta**:
    ```json
    {
        "user_id": "uuid",
        "permission": "users.create",
        "has_permission": true
    }
    ```
    
    **Nota**: Usuários podem verificar suas próprias permissões.
    Para verificar de outros usuários, requer: permissions.read
    """
    try:
        # Verificar se está checando próprias permissões ou de outro usuário
        if str(user_id) != str(current_user.id):
            # Verificar se tem permissão para checar de outros
            if not any(
                perm.nome == "permissions.read"
                for role in current_user.roles
                for perm in role.permissions
            ):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={"error": "forbidden", "message": "Sem permissão"}
                )
        
        logger.info(f"Checking if user {user_id} has permission {permission_name}")
        has_permission = await usecase.execute(str(user_id), permission_name)
        
        return {
            "user_id": str(user_id),
            "permission": permission_name,
            "has_permission": has_permission
        }
        
    except Exception as e:
        logger.error(f"Error checking permission: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao verificar permissão"}
        )


@router.get(
    "/me",
    response_model=List[PermissionResponseDTO],
    summary="Minhas permissões",
    description="Lista todas as permissões do usuário autenticado",
    responses={
        200: {"description": "Lista de permissões"},
        401: {"description": "Não autenticado"}
    }
)
async def get_my_permissions(
    usecase: GetUserPermissionsUseCase = Depends(get_get_user_permissions_usecase),
    current_user: UserResponseDTO = Depends(get_current_user)
) -> List[PermissionResponseDTO]:
    """
    Lista todas as permissões do usuário autenticado.
    
    Útil para verificar quais ações o usuário pode realizar.
    """
    try:
        logger.info(f"Getting permissions for current user: {current_user.id}")
        permissions = await usecase.execute(str(current_user.id))
        return permissions
        
    except Exception as e:
        logger.error(f"Error getting my permissions: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"error": "internal_error", "message": "Erro ao buscar permissões"}
        )


# ============================================================================
# STATISTICS & REPORTS
# ============================================================================

@router.get(
    "/stats",
    response_model=PermissionStatsDTO,
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
    current_user: UserResponseDTO = Depends(require_permission("permissions.read"))
) -> PermissionStatsDTO:
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
        
        stats = PermissionStatsDTO(
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

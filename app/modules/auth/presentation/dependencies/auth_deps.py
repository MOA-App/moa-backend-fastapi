from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.application.usecases.permission.bulk_create_permissions_usecase import BulkCreatePermissionsUseCase
from app.modules.auth.application.usecases.permission.create_permission_usecase import CreatePermissionUseCase
from app.modules.auth.application.usecases.permission.delete_permission_usecase import DeletePermissionUseCase
from app.modules.auth.application.usecases.permission.get_permission_usecase import GetPermissionUseCase
from app.modules.auth.application.usecases.permission.list_permissions_usecase import ListPermissionsUseCase
from app.modules.auth.application.usecases.permission.list_resources_usecase import ListResourcesUseCase
from app.modules.auth.application.usecases.permission.update_permission_usecase import UpdatePermissionUseCase
from app.shared.infrastructure.database.session import get_db

# Repositories
from ...infrastructure.repositories.permission_repository_impl import PermissionRepositoryImpl

"""
Dependencies (Injeção de Dependências) para Permission.

Responsável por criar e fornecer instâncias dos Use Cases
com suas dependências (repositories, services, etc.)
"""

# ============================================================================
# REPOSITORY DEPENDENCIES
# ============================================================================

def get_permission_repository(
    db: AsyncSession = Depends(get_db)
) -> PermissionRepositoryImpl:
    """Dependency para obter Permission Repository"""
    return PermissionRepositoryImpl(db)


def get_role_repository(
    db: AsyncSession = Depends(get_db)
) -> RoleRepositoryImpl:
    """Dependency para obter Role Repository"""
    return RoleRepositoryImpl(db)


def get_user_repository(
    db: AsyncSession = Depends(get_db)
) -> UserRepositoryImpl:
    """Dependency para obter User Repository"""
    return UserRepositoryImpl(db)


# ============================================================================
# USE CASE DEPENDENCIES - CRUD
# ============================================================================

def get_create_permission_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> CreatePermissionUseCase:
    """Dependency para CreatePermissionUseCase"""
    return CreatePermissionUseCase(permission_repo)


def get_permission_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> GetPermissionUseCase:
    """Dependency para GetPermissionUseCase"""
    return GetPermissionUseCase(permission_repo)


def get_list_permissions_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> ListPermissionsUseCase:
    """Dependency para ListPermissionsUseCase"""
    return ListPermissionsUseCase(permission_repo)


def get_update_permission_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> UpdatePermissionUseCase:
    """Dependency para UpdatePermissionUseCase"""
    return UpdatePermissionUseCase(permission_repo)


def get_delete_permission_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> DeletePermissionUseCase:
    """Dependency para DeletePermissionUseCase"""
    return DeletePermissionUseCase(permission_repo)


# ============================================================================
# USE CASE DEPENDENCIES - BULK & RESOURCES
# ============================================================================

def get_bulk_create_permissions_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> BulkCreatePermissionsUseCase:
    """Dependency para BulkCreatePermissionsUseCase"""
    return BulkCreatePermissionsUseCase(permission_repo)


def get_list_resources_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository)
) -> ListResourcesUseCase:
    """Dependency para ListResourcesUseCase"""
    return ListResourcesUseCase(permission_repo)


# ============================================================================
# USE CASE DEPENDENCIES - ROLE OPERATIONS
# ============================================================================

def get_assign_permission_to_role_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository),
    role_repo: RoleRepositoryImpl = Depends(get_role_repository)
) -> AssignPermissionToRoleUseCase:
    """Dependency para AssignPermissionToRoleUseCase"""
    return AssignPermissionToRoleUseCase(permission_repo, role_repo)


def get_revoke_permission_from_role_usecase(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository),
    role_repo: RoleRepositoryImpl = Depends(get_role_repository)
) -> RevokePermissionFromRoleUseCase:
    """Dependency para RevokePermissionFromRoleUseCase"""
    return RevokePermissionFromRoleUseCase(permission_repo, role_repo)


def get_role_permissions_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository)
) -> GetRolePermissionsUseCase:
    """Dependency para GetRolePermissionsUseCase"""
    return GetRolePermissionsUseCase(role_repo)


# ============================================================================
# USE CASE DEPENDENCIES - USER OPERATIONS
# ============================================================================

def get_check_user_permission_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository)
) -> CheckUserPermissionUseCase:
    """Dependency para CheckUserPermissionUseCase"""
    return CheckUserPermissionUseCase(user_repo)


def get_user_permissions_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository)
) -> GetUserPermissionsUseCase:
    """Dependency para GetUserPermissionsUseCase"""
    return GetUserPermissionsUseCase(user_repo)


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_all_permission_usecases(
    permission_repo: PermissionRepositoryImpl = Depends(get_permission_repository),
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
    user_repo: UserRepositoryImpl = Depends(get_user_repository)
) -> dict:
    """
    Retorna dicionário com todos os use cases de Permission.
    
    Útil para cenários onde múltiplos use cases são necessários.
    
    Returns:
        dict: Dicionário com use cases
    """
    return {
        "create": CreatePermissionUseCase(permission_repo),
        "get": GetPermissionUseCase(permission_repo),
        "list": ListPermissionsUseCase(permission_repo),
        "update": UpdatePermissionUseCase(permission_repo),
        "delete": DeletePermissionUseCase(permission_repo),
        "bulk_create": BulkCreatePermissionsUseCase(permission_repo),
        "list_resources": ListResourcesUseCase(permission_repo),
        "assign_to_role": AssignPermissionToRoleUseCase(permission_repo, role_repo),
        "revoke_from_role": RevokePermissionFromRoleUseCase(permission_repo, role_repo),
        "get_role_permissions": GetRolePermissionsUseCase(role_repo),
        "check_user_permission": CheckUserPermissionUseCase(user_repo),
        "get_user_permissions": GetUserPermissionsUseCase(user_repo),
    }

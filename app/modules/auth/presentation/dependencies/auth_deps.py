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

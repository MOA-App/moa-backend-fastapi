from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.application.usecases.role.addpermission_role_usecase import AddPermissionToRoleUseCase
from app.modules.auth.application.usecases.role.get_role_by_id_usecase import GetRoleByIdUseCase
from app.modules.auth.application.usecases.role.create_role_usecase import CreateRoleUseCase
from app.modules.auth.application.usecases.role.delete_role_usecase import DeleteRoleUseCase
from app.modules.auth.application.usecases.role.list_roles_usecase import ListRolesUseCase
from app.modules.auth.application.usecases.role.remove_permission_from_role_usecase import RemovePermissionFromRoleUseCase
from app.modules.auth.application.usecases.role.update_role_usecase import UpdateRoleUseCase
from app.shared.infrastructure.database.session import get_db

from app.modules.auth.infrastructure.repositories.role_repository_impl import RoleRepositoryImpl


"""
Dependencies (Injeção de Dependências) para Role.

Responsável por criar e fornecer instâncias dos Use Cases
com suas dependências (repositories, services, etc.)
"""


# ============================================================================
# REPOSITORY DEPENDENCY
# ============================================================================

def get_role_repository(
    db: AsyncSession = Depends(get_db),
) -> RoleRepositoryImpl:
    """Dependency para obter Role Repository."""
    return RoleRepositoryImpl(db)


# ============================================================================
# USE CASE DEPENDENCIES - CRUD
# ============================================================================

def get_create_role_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> CreateRoleUseCase:
    """Dependency para CreateRoleUseCase."""
    return CreateRoleUseCase(role_repo)


def get_role_by_id_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> GetRoleByIdUseCase:
    """Dependency para GetRoleByIdUseCase."""
    return GetRoleByIdUseCase(role_repo)


def get_list_roles_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> ListRolesUseCase:
    """Dependency para ListRolesUseCase."""
    return ListRolesUseCase(role_repo)


def get_update_role_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> UpdateRoleUseCase:
    """Dependency para UpdateRoleUseCase."""
    return UpdateRoleUseCase(role_repo)


def get_delete_role_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> DeleteRoleUseCase:
    """Dependency para DeleteRoleUseCase."""
    return DeleteRoleUseCase(role_repo)


# ============================================================================
# USE CASE DEPENDENCIES - PERMISSIONS
# ============================================================================

def get_add_permission_to_role_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> AddPermissionToRoleUseCase:
    """Dependency para AddPermissionToRoleUseCase."""
    return AddPermissionToRoleUseCase(role_repo)


def get_remove_permission_from_role_usecase(
    role_repo: RoleRepositoryImpl = Depends(get_role_repository),
) -> RemovePermissionFromRoleUseCase:
    """Dependency para RemovePermissionFromRoleUseCase."""
    return RemovePermissionFromRoleUseCase(role_repo)

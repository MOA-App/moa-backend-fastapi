from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.auth.application.usecases.user.create_user import CreateUserUseCase
from app.modules.auth.application.usecases.user.delete_user import DeleteUserUseCase
from app.modules.auth.application.usecases.user.get_user_by_email import GetUserByEmailUseCase
from app.modules.auth.application.usecases.user.get_user_by_id import GetUserByIdUseCase
from app.modules.auth.application.usecases.user.update_user import UpdateUserUseCase
from app.shared.infrastructure.database.session import get_db

from app.modules.auth.infrastructure.repositories.user_repository_impl import (
    UserRepositoryImpl,
)


"""
Dependencies (Injeção de Dependências) para User.

Responsável por criar e fornecer instâncias dos Use Cases
com suas dependências (repositories, services, etc.)
"""


# ============================================================================
# REPOSITORY DEPENDENCY
# ============================================================================

def get_user_repository(
    db: AsyncSession = Depends(get_db),
) -> UserRepositoryImpl:
    """Dependency para obter User Repository."""
    return UserRepositoryImpl(db)


# ============================================================================
# USE CASE DEPENDENCIES - CRUD
# ============================================================================

def get_create_user_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> CreateUserUseCase:
    """Dependency para CreateUserUseCase."""
    return CreateUserUseCase(user_repo)


def get_user_by_id_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> GetUserByIdUseCase:
    """Dependency para GetUserByIdUseCase."""
    return GetUserByIdUseCase(user_repo)


def get_user_by_email_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> GetUserByEmailUseCase:
    """Dependency para GetUserByEmailUseCase."""
    return GetUserByEmailUseCase(user_repo)


def get_update_user_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> UpdateUserUseCase:
    """Dependency para UpdateUserUseCase."""
    return UpdateUserUseCase(user_repo)


def get_delete_user_usecase(
    user_repo: UserRepositoryImpl = Depends(get_user_repository),
) -> DeleteUserUseCase:
    """Dependency para DeleteUserUseCase."""
    return DeleteUserUseCase(user_repo)

from uuid import UUID

from fastapi import APIRouter, Depends, status



from app.modules.auth.application.dtos.user.create_user_request_dto import CreateUserRequest as CreateUserDTO
from app.modules.auth.application.dtos.user.update_user_request_dto import UpdateUserRequest as UpdateUserDTO
from app.modules.auth.presentation.schemas.user.user_request import AssignRoleRequest, CreateUserRequest, UpdateUserRequest
from app.modules.auth.presentation.schemas.user.user_response import UserListResponse, UserResponse
from app.modules.auth.application.usecases.user.create_user import CreateUserUseCase
from app.modules.auth.application.usecases.user.delete_user import DeleteUserUseCase
from app.modules.auth.application.usecases.user.get_user_by_email import GetUserByEmailUseCase
from app.modules.auth.application.usecases.user.get_user_by_id import GetUserByIdUseCase
from app.modules.auth.application.usecases.user.update_user import UpdateUserUseCase
from app.modules.auth.presentation.dependencies.permissions import (
    require_permission,
)
from app.modules.auth.presentation.dependencies.user import (
    get_create_user_usecase,
    get_delete_user_usecase,
    get_user_by_email_usecase,
    get_user_by_id_usecase,
    get_list_users_usecase,
    get_update_user_usecase,
    get_assign_role_to_user_usecase,
    get_remove_role_from_user_usecase,
)
from app.modules.auth.application.usecases.user.assign_role_to_user import AssignRoleToUserUseCase
from app.modules.auth.application.usecases.user.remove_role_from_user import RemoveRoleFromUserUseCase

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def _to_response(user) -> UserResponse:
    return UserResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        is_active=user.is_active,
        roles=user.roles,
        created_at=user.created_at,
    )


# ============================================================================
# CREATE
# ============================================================================

@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_permission("users:create"))],
)
async def create_user(
    request: CreateUserRequest,
    usecase: CreateUserUseCase = Depends(get_create_user_usecase),
):
    dto = CreateUserDTO(
        name=request.name,
        email=request.email,
        password=request.password,
    )

    user = await usecase.execute(dto.name, dto.email, dto.password)

    return _to_response(user)


@router.get(
    "/",
    response_model=UserListResponse,
    dependencies=[Depends(require_permission("users.read"))],
)
async def list_users(
    usecase=Depends(get_list_users_usecase),
):
    users = await usecase.execute()
    return UserListResponse(users=[_to_response(user) for user in users])


# ============================================================================
# GET BY ID
# ============================================================================

@router.get(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users:read"))],
)
async def get_user(
    user_id: UUID,
    usecase: GetUserByIdUseCase = Depends(get_user_by_id_usecase),
):
    user = await usecase.execute(str(user_id))

    return _to_response(user)


# ============================================================================
# GET BY EMAIL
# ============================================================================

@router.get(
    "/email/{email}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users:read"))],
)
async def get_user_by_email(
    email: str,
    usecase: GetUserByEmailUseCase = Depends(
        get_user_by_email_usecase,
    ),
):
    user = await usecase.execute(email)

    return _to_response(user)


# ============================================================================
# UPDATE
# ============================================================================

@router.put(
    "/{user_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users:update"))],
)
async def update_user(
    user_id: UUID,
    request: UpdateUserRequest,
    usecase: UpdateUserUseCase = Depends(get_update_user_usecase),
):
    dto = UpdateUserDTO(
        name=request.name,
        email=request.email,
        password=request.password,
        is_active=request.is_active,
    )

    user = await usecase.execute(str(user_id), dto)

    return _to_response(user)


# ============================================================================
# DELETE
# ============================================================================

@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(require_permission("users:delete"))],
)
async def delete_user(
    user_id: UUID,
    usecase: DeleteUserUseCase = Depends(get_delete_user_usecase),
):
    await usecase.execute(str(user_id))


@router.post(
    "/{user_id}/roles",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.update"))],
)
async def assign_role(
    user_id: UUID,
    request: AssignRoleRequest,
    usecase: AssignRoleToUserUseCase = Depends(get_assign_role_to_user_usecase),
):
    user = await usecase.execute(str(user_id), request.role_id)
    return _to_response(user)


@router.delete(
    "/{user_id}/roles/{role_id}",
    response_model=UserResponse,
    dependencies=[Depends(require_permission("users.update"))],
)
async def remove_role(
    user_id: UUID,
    role_id: UUID,
    usecase: RemoveRoleFromUserUseCase = Depends(get_remove_role_from_user_usecase),
):
    user = await usecase.execute(str(user_id), str(role_id))
    return _to_response(user)

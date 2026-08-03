from uuid import UUID

from fastapi import APIRouter, Depends, status



from app.modules.auth.application.dtos.user.create_user_request_dto import CreateUserRequest
from app.modules.auth.application.dtos.user.update_user_request_dto import UpdateUserRequest
from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
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
    get_get_user_by_email_usecase,
    get_get_user_by_id_usecase,
    get_list_users_usecase,
    get_update_user_usecase,
)

router = APIRouter(
    prefix="/users",
    tags=["Users"],
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
    dto = UserResponse(
        name=request.name,
        email=request.email,
    )

    user = await usecase.execute(dto)

    return UserResponse.model_validate(user)


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
    usecase: GetUserByIdUseCase = Depends(get_get_user_by_id_usecase),
):
    user = await usecase.execute(user_id)

    return UserResponse.model_validate(user)


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
        get_get_user_by_email_usecase,
    ),
):
    user = await usecase.execute(email)

    return UserResponse.model_validate(user)


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
    dto = UserResponse(
        id=user_id,
        name=request.name,
        email=request.email,
        password=request.password,
        is_active=request.is_active,
    )

    user = await usecase.execute(dto)

    return UserResponse.model_validate(user)


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
    await usecase.execute(user_id)

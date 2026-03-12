from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.modules.auth.application.dtos.role.role_inputs import AddPermissionToRoleDTO, CreateRoleDTO, RemovePermissionFromRoleDTO, UpdateRoleDTO
from app.modules.auth.application.usecases.role.create_role_usecase import CreateRoleUseCase
from app.modules.auth.application.usecases.role.get_role_by_id_usecase import GetRoleByIdUseCase
from app.modules.auth.application.usecases.role.list_roles_usecase import ListRolesUseCase
from app.modules.auth.application.usecases.role.update_role_usecase import UpdateRoleUseCase
from app.modules.auth.application.usecases.role.delete_role_usecase import DeleteRoleUseCase
from app.modules.auth.application.usecases.role.add_permission_to_role_usecase import AddPermissionToRoleUseCase
from app.modules.auth.application.usecases.role.remove_permission_from_role_usecase import RemovePermissionFromRoleUseCase

from app.modules.auth.presentation.dependencies.permissions import require_permission
from app.modules.auth.presentation.schemas.role.add_permission_role_request import AddPermissionToRoleRequest
from app.modules.auth.presentation.schemas.role.create_role_request import CreateRoleRequest
from app.modules.auth.presentation.schemas.role.update_role_request import UpdateRoleRequest
from app.modules.auth.presentation.utils.response_util import ResponseUtil

from ..dependencies.role import (
    get_create_role_usecase,
    get_role_by_id_usecase,
    get_list_roles_usecase,
    get_update_role_usecase,
    get_delete_role_usecase,
    get_add_permission_to_role_usecase,
    get_remove_permission_from_role_usecase,
)

router = APIRouter(prefix="/roles", tags=["Roles"])


# ============================================================================
# CRUD
# ============================================================================

@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Criar role",
    dependencies=[Depends(require_permission("roles.create"))],
)
async def create_role(
    body: CreateRoleRequest,
    usecase: CreateRoleUseCase = Depends(get_create_role_usecase),
):
    dto = CreateRoleDTO(name=body.nome)

    result = await usecase.execute(dto)

    return ResponseUtil.created(
        data=result,
        message="Role criada com sucesso",
    )


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Listar todas as roles",
    dependencies=[Depends(require_permission("roles.list"))],
)
async def list_roles(
    usecase: ListRolesUseCase = Depends(get_list_roles_usecase),
):
    result = await usecase.execute()
    return ResponseUtil.success(data=result)


@router.get(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar role por ID",
    dependencies=[Depends(require_permission("roles.read"))],
)
async def get_role(
    role_id: UUID,
    usecase: GetRoleByIdUseCase = Depends(get_role_by_id_usecase),
):
    result = await usecase.execute(role_id)
    return ResponseUtil.success(data=result)


@router.put(
    "/{role_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar role",
    dependencies=[Depends(require_permission("roles.update"))],
)
async def update_role(
    role_id: UUID,
    body: UpdateRoleRequest,
    usecase: UpdateRoleUseCase = Depends(get_update_role_usecase),
):
    dto = UpdateRoleDTO(role_id=role_id, name=body.nome)
    result = await usecase.execute(dto)
    return ResponseUtil.success(
        data=result,
        message="Role atualizada com sucesso",
    )


@router.delete(
    "/{role_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover role",
    dependencies=[Depends(require_permission("roles.delete"))],
)
async def delete_role(
    role_id: UUID,
    usecase: DeleteRoleUseCase = Depends(get_delete_role_usecase),
):
    await usecase.execute(role_id)
    return ResponseUtil.no_content()


# ============================================================================
# PERMISSIONS
# ============================================================================

@router.post(
    "/{role_id}/permissions",
    status_code=status.HTTP_200_OK,
    summary="Associar permissão à role",
    dependencies=[Depends(require_permission("roles.assign_permission"))],
)
async def add_permission_to_role(
    role_id: UUID,
    body: AddPermissionToRoleRequest,
    usecase: AddPermissionToRoleUseCase = Depends(get_add_permission_to_role_usecase),
):
    dto = AddPermissionToRoleDTO(role_id=role_id, permission_id=body.permission_id)
    await usecase.execute(dto)
    return ResponseUtil.success(message="Permissão associada com sucesso", data=None)


@router.delete(
    "/{role_id}/permissions/{permission_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover permissão da role",
    dependencies=[Depends(require_permission("roles.remove_permission"))],
)
async def remove_permission_from_role(
    role_id: UUID,
    permission_id: UUID,
    usecase: RemovePermissionFromRoleUseCase = Depends(get_remove_permission_from_role_usecase),
):
    dto = RemovePermissionFromRoleDTO(role_id=role_id, permission_id=permission_id)
    await usecase.execute(dto)
    return ResponseUtil.no_content()

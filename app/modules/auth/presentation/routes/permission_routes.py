from fastapi import APIRouter, Depends, HTTPException
from uuid import UUID

from app.modules.auth.application.dtos.permission.permission_bulk import BulkCreatePermissionsDTO
from app.modules.auth.application.dtos.permission.permission_inputs import (
    CreatePermissionDTO,
    UpdatePermissionDTO,
)
from app.modules.auth.application.usecases.permission.bulk_create_permissions_usecase import BulkCreatePermissionsUseCase
from app.modules.auth.application.usecases.permission.create_permission_usecase import CreatePermissionUseCase
from app.modules.auth.application.usecases.permission.delete_permission_usecase import DeletePermissionUseCase
from app.modules.auth.application.usecases.permission.get_permission_usecase import GetPermissionUseCase
from app.modules.auth.application.usecases.permission.get_permission_by_name_usecase import GetPermissionByNameUseCase
from app.modules.auth.application.usecases.permission.list_permissions_usecase import ListPermissionsUseCase
from app.modules.auth.application.usecases.permission.list_resources_usecase import ListResourcesUseCase
from app.modules.auth.application.usecases.permission.update_permission_usecase import UpdatePermissionUseCase

from app.modules.auth.domain.exceptions.auth_exceptions import (
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
    InvalidPermissionFormatException,
)

from app.modules.auth.presentation.schemas.permission.create_permission_schema import CreatePermissionRequest
from app.modules.auth.presentation.schemas.permission.update_permission_schema import UpdatePermissionRequest
from app.modules.auth.presentation.schemas.permission.bulk_create_request_schema import BulkCreatePermissionsRequest
from app.modules.auth.presentation.schemas.permission.permission_response import PermissionResponse

from ..dependencies.auth_deps import (
    get_bulk_create_permissions_usecase,
    get_create_permission_usecase,
    get_delete_permission_usecase,
    get_list_permissions_usecase,
    get_list_resources_usecase,
    get_permission_usecase,
    get_permission_by_name_usecase,
    get_update_permission_usecase,
)

router = APIRouter(prefix="/permissions", tags=["Permissions"])


# ================= CREATE =================

@router.post("", status_code=201)
async def create_permission(
    body: CreatePermissionRequest,
    usecase: CreatePermissionUseCase = Depends(get_create_permission_usecase),
):
    try:
        dto = CreatePermissionDTO(
            nome=body.nome,
            descricao=body.descricao,
        )
        result = await usecase.execute(dto)
        return {"success": True, "data": result}

    except PermissionAlreadyExistsException:
        raise HTTPException(status_code=409, detail="Permissão já existe")

    except InvalidPermissionFormatException:
        raise HTTPException(status_code=400, detail="Formato inválido")


# ================= LIST =================

@router.get("")
async def list_permissions(
    usecase: ListPermissionsUseCase = Depends(get_list_permissions_usecase),
):
    result = await usecase.execute()
    return {"success": True, "data": result}


# ================= GET =================

@router.get("/{permission_id}")
async def get_permission(
    permission_id: UUID,
    usecase: GetPermissionUseCase = Depends(get_permission_usecase),
):
    try:
        result = await usecase.execute(str(permission_id))
        return {"success": True, "data": result}

    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")


# ================= GET BY NAME =================

@router.get("/search/by-name", response_model=PermissionResponse)
async def get_permission_by_name(
    name: str,
    usecase: GetPermissionByNameUseCase = Depends(get_permission_by_name_usecase),
):
    try:
        result = await usecase.execute(name)
        return result

    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")


# ================= UPDATE =================

@router.put("/{permission_id}")
async def update_permission(
    permission_id: UUID,
    body: UpdatePermissionRequest,
    usecase: UpdatePermissionUseCase = Depends(get_update_permission_usecase),
):
    try:
        dto = UpdatePermissionDTO(descricao=body.descricao)
        result = await usecase.execute(str(permission_id), dto)
        return {"success": True, "data": result}

    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")


# ================= DELETE =================

@router.delete("/{permission_id}", status_code=204)
async def delete_permission(
    permission_id: UUID,
    usecase: DeletePermissionUseCase = Depends(get_delete_permission_usecase),
):
    try:
        await usecase.execute(str(permission_id))

    except PermissionNotFoundException:
        raise HTTPException(status_code=404, detail="Permissão não encontrada")


# ================= BULK =================

@router.post("/bulk", status_code=201)
async def bulk_create_permissions(
    body: BulkCreatePermissionsRequest,
    usecase: BulkCreatePermissionsUseCase = Depends(get_bulk_create_permissions_usecase),
):
    if not body.permissions:
        raise HTTPException(status_code=400, detail="Lista vazia")

    dto = BulkCreatePermissionsDTO(
        permissions=[
            CreatePermissionDTO(nome=p.nome, descricao=p.descricao)
            for p in body.permissions
        ]
    )

    result = await usecase.execute(dto)
    return {"success": True, "data": result}


# ================= RESOURCES =================

@router.get("/resources/list")
async def list_resources(
    usecase: ListResourcesUseCase = Depends(get_list_resources_usecase),
):
    result = await usecase.execute()
    return {"success": True, "data": result}

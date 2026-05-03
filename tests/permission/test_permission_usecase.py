import pytest
from uuid import uuid4

from app.modules.auth.application.dtos.permission.permission_inputs import CreatePermissionDTO, UpdatePermissionDTO
from app.modules.auth.application.dtos.permission.permission_bulk import BulkCreatePermissionsDTO

from app.modules.auth.application.usecases.permission.create_permission_usecase import CreatePermissionUseCase
from app.modules.auth.application.usecases.permission.get_permission_usecase import GetPermissionUseCase
from app.modules.auth.application.usecases.permission.list_permissions_usecase import ListPermissionsUseCase
from app.modules.auth.application.usecases.permission.list_resources_usecase import ListResourcesUseCase
from app.modules.auth.application.usecases.permission.update_permission_usecase import UpdatePermissionUseCase
from app.modules.auth.application.usecases.permission.delete_permission_usecase import DeletePermissionUseCase
from app.modules.auth.application.usecases.permission.bulk_create_permissions_usecase import BulkCreatePermissionsUseCase

from app.modules.auth.domain.exceptions.auth_exceptions import (
    PermissionAlreadyExistsException,
    PermissionNotFoundException,
)
from tests.permission.test_permission_entity import make_permission


# ============================================================================
# CREATE
# ============================================================================

class TestCreatePermissionUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return CreatePermissionUseCase(mock_permission_repository)

    async def test_creates_permission_successfully(self, usecase, mock_permission_repository):
        perm = make_permission("users.create")
        mock_permission_repository.exists_by_name.return_value = False
        mock_permission_repository.create.return_value = perm

        dto = CreatePermissionDTO(nome="users.create", descricao=None)

        result = await usecase.execute(dto)

        mock_permission_repository.create.assert_awaited_once()
        assert result is not None

    async def test_raises_if_name_already_exists(self, usecase, mock_permission_repository):
        mock_permission_repository.exists_by_name.return_value = True

        dto = CreatePermissionDTO(nome="users.create", descricao=None)

        with pytest.raises(PermissionAlreadyExistsException):
            await usecase.execute(dto)

        mock_permission_repository.create.assert_not_awaited()


# ============================================================================
# GET BY ID
# ============================================================================

class TestGetPermissionUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return GetPermissionUseCase(mock_permission_repository)

    async def test_returns_permission_when_found(self, usecase, mock_permission_repository):
        perm = make_permission("users.read")
        mock_permission_repository.find_by_id.return_value = perm

        result = await usecase.execute(str(perm.id.value))

        assert result is not None
        mock_permission_repository.find_by_id.assert_awaited_once()

    async def test_raises_when_not_found(self, usecase, mock_permission_repository):
        mock_permission_repository.find_by_id.return_value = None

        with pytest.raises(PermissionNotFoundException):
            await usecase.execute(str(uuid4()))


# ============================================================================
# LIST ALL
# ============================================================================

class TestListPermissionsUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return ListPermissionsUseCase(mock_permission_repository)

    async def test_returns_all_permissions(self, usecase, mock_permission_repository):
        perms = [
            make_permission("users.create"),
            make_permission("users.read"),
            make_permission("posts.delete"),
        ]
        mock_permission_repository.list_all.return_value = perms

        result = await usecase.execute()

        assert len(result.items) == 3
        assert result.total == 3
        mock_permission_repository.list_all.assert_awaited_once()

    async def test_returns_empty_list(self, usecase, mock_permission_repository):
        mock_permission_repository.list_all.return_value = []

        result = await usecase.execute()

        assert result.items == []
        assert result.total == 0


# ============================================================================
# LIST RESOURCES
# ============================================================================

class TestListResourcesUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return ListResourcesUseCase(mock_permission_repository)

    async def test_returns_unique_resources(self, usecase, mock_permission_repository):
        mock_permission_repository.list_resources.return_value = ["posts", "users"]

        result = await usecase.execute()

        assert result == ["posts", "users"]
        mock_permission_repository.list_resources.assert_awaited_once()

    async def test_returns_empty_when_no_permissions(self, usecase, mock_permission_repository):
        mock_permission_repository.list_resources.return_value = []

        result = await usecase.execute()

        assert result == []


# ============================================================================
# UPDATE
# ============================================================================

class TestUpdatePermissionUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return UpdatePermissionUseCase(mock_permission_repository)

    async def test_updates_description_successfully(self, usecase, mock_permission_repository):
        perm = make_permission("users.create", descricao="Antiga")
        updated = make_permission("users.create", descricao="Nova", with_id=perm.id)

        mock_permission_repository.find_by_id.return_value = perm
        mock_permission_repository.update.return_value = updated

        dto = UpdatePermissionDTO(descricao="Nova")

        result = await usecase.execute(str(perm.id.value), dto)

        mock_permission_repository.update.assert_awaited_once()
        assert result is not None

    async def test_raises_when_not_found(self, usecase, mock_permission_repository):
        mock_permission_repository.find_by_id.return_value = None

        with pytest.raises(PermissionNotFoundException):
            await usecase.execute(str(uuid4()), {"descricao": "Nova"})

        mock_permission_repository.update.assert_not_awaited()


# ============================================================================
# DELETE
# ============================================================================

class TestDeletePermissionUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return DeletePermissionUseCase(mock_permission_repository)

    async def test_deletes_successfully(self, usecase, mock_permission_repository):
        perm = make_permission("users.delete")
        mock_permission_repository.find_by_id.return_value = perm

        await usecase.execute(str(perm.id.value))

        mock_permission_repository.delete.assert_awaited_once()

    async def test_raises_when_not_found(self, usecase, mock_permission_repository):
        mock_permission_repository.find_by_id.return_value = None

        with pytest.raises(PermissionNotFoundException):
            await usecase.execute(str(uuid4()))

        mock_permission_repository.delete.assert_not_awaited()


# ============================================================================
# BULK CREATE
# ============================================================================

class TestBulkCreatePermissionsUseCase:

    @pytest.fixture
    def usecase(self, mock_permission_repository):
        return BulkCreatePermissionsUseCase(mock_permission_repository)

    async def test_creates_multiple_permissions(self, usecase, mock_permission_repository):
        perms = [
            make_permission("users.create"),
            make_permission("users.read"),
            make_permission("users.delete"),
        ]

        mock_permission_repository.find_by_name.return_value = None
        mock_permission_repository.create.side_effect = perms

        dto = BulkCreatePermissionsDTO(
            permissions=[
                CreatePermissionDTO(nome="users.create"),
                CreatePermissionDTO(nome="users.read"),
                CreatePermissionDTO(nome="users.delete"),
            ]
        )

        result = await usecase.execute(dto)

        assert mock_permission_repository.create.await_count == 3
        assert result.total_created == 3

    async def test_skips_existing_permissions(self, usecase, mock_permission_repository):
        mock_permission_repository.exists_by_name.return_value = True

        dto = BulkCreatePermissionsDTO(
            permissions=[
                CreatePermissionDTO(nome="users.create"),
                CreatePermissionDTO(nome="users.read"),
            ]
        )

        result = await usecase.execute(dto)

        mock_permission_repository.create.assert_not_awaited()
        assert result.total_skipped == 2

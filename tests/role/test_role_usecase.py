import pytest
from uuid import uuid4

from app.modules.auth.application.usecases.role.create_role_usecase import CreateRoleUseCase
from app.modules.auth.application.usecases.role.get_role_by_id_usecase import GetRoleByIdUseCase
from app.modules.auth.application.usecases.role.list_roles_usecase import ListRolesUseCase
from app.modules.auth.application.usecases.role.update_role_usecase import UpdateRoleUseCase
from app.modules.auth.application.usecases.role.delete_role_usecase import DeleteRoleUseCase
from app.modules.auth.application.dtos.role.role_inputs import CreateRoleDTO, UpdateRoleDTO

from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.exceptions.auth_exceptions import (
    RoleAlreadyExistsException,
    RoleNotFoundException,
)
from app.shared.domain.value_objects.id_vo import EntityId

from app.modules.auth.domain.value_objects.role_name_vo import RoleName

def make_role(name: str, with_id: EntityId | None = None):
    return Role(
        id=with_id or EntityId(str(uuid4())),
        nome=RoleName(name),
        _permissions=[],
    )
# ============================================================================
# CREATE
# ============================================================================

class TestCreateRoleUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return CreateRoleUseCase(mock_role_repository)

    async def test_creates_role_successfully(self, usecase, mock_role_repository):
        role = make_role("admin")
        mock_role_repository.exists_by_name.return_value = False
        mock_role_repository.create.return_value = role

        result = await usecase.execute(CreateRoleDTO(name="admin"))

        mock_role_repository.create.assert_awaited_once()
        assert result is not None

    async def test_raises_if_name_already_exists(self, usecase, mock_role_repository):
        mock_role_repository.exists_by_name.return_value = True

        with pytest.raises(RoleAlreadyExistsException):
            await usecase.execute(CreateRoleDTO(name="admin"))

        mock_role_repository.create.assert_not_awaited()


# ============================================================================
# GET BY ID
# ============================================================================

class TestGetRoleByIdUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return GetRoleByIdUseCase(mock_role_repository)

    async def test_returns_role_when_found(self, usecase, mock_role_repository):
        role = make_role("admin")
        mock_role_repository.find_by_id.return_value = role

        result = await usecase.execute(role.id.value)

        assert result is not None
        mock_role_repository.find_by_id.assert_awaited_once()

    async def test_raises_when_not_found(self, usecase, mock_role_repository):
        mock_role_repository.find_by_id.return_value = None

        with pytest.raises(RoleNotFoundException):
            await usecase.execute(uuid4())


# ============================================================================
# LIST
# ============================================================================

class TestListRolesUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return ListRolesUseCase(mock_role_repository)

    async def test_returns_all_roles(self, usecase, mock_role_repository):
        roles = [make_role("admin"), make_role("editor"), make_role("viewer")]
        mock_role_repository.list_all.return_value = roles

        result = await usecase.execute()

        assert result.total == 3
        assert len(result.roles) == 3

    async def test_returns_empty_list(self, usecase, mock_role_repository):
        mock_role_repository.list_all.return_value = []

        result = await usecase.execute()

        assert result.total == 0
        assert result.roles == []


# ============================================================================
# UPDATE
# ============================================================================

class TestUpdateRoleUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return UpdateRoleUseCase(mock_role_repository)

    async def test_updates_name_successfully(self, usecase, mock_role_repository):
        role = make_role("editor")
        updated_role = make_role("super_editor", with_id=role.id)

        mock_role_repository.find_by_id.return_value = role
        mock_role_repository.find_by_name.return_value = None
        mock_role_repository.update.return_value = updated_role

        result = await usecase.execute(
            UpdateRoleDTO(role_id=role.id.value, name="super_editor")
        )

        mock_role_repository.update.assert_awaited_once()
        assert result is not None

    async def test_raises_when_role_not_found(self, usecase, mock_role_repository):
        mock_role_repository.find_by_id.return_value = None

        with pytest.raises(RoleNotFoundException):
            await usecase.execute(UpdateRoleDTO(role_id=uuid4(), name="any"))

    async def test_raises_when_new_name_already_taken(self, usecase, mock_role_repository):
        role = make_role("editor")
        other_role = make_role("super_editor")

        mock_role_repository.find_by_id.return_value = role
        mock_role_repository.find_by_name.return_value = other_role  # nome ocupado por outra role

        with pytest.raises(RoleAlreadyExistsException):
            await usecase.execute(
                UpdateRoleDTO(role_id=role.id.value, name="super_editor")
            )

        mock_role_repository.update.assert_not_awaited()

    async def test_allows_update_to_same_name(self, usecase, mock_role_repository):
        """Atualizar para o mesmo nome da própria role não deve lançar conflito."""
        role = make_role("editor")
        mock_role_repository.find_by_id.return_value = role
        mock_role_repository.find_by_name.return_value = role  # retorna a mesma role
        mock_role_repository.update.return_value = role

        result = await usecase.execute(
            UpdateRoleDTO(role_id=role.id.value, name="editor")
        )

        mock_role_repository.update.assert_awaited_once()
        assert result is not None


# ============================================================================
# DELETE
# ============================================================================

class TestDeleteRoleUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return DeleteRoleUseCase(mock_role_repository)

    async def test_deletes_successfully(self, usecase, mock_role_repository):
        role = make_role("admin")
        mock_role_repository.find_by_id.return_value = role

        await usecase.execute(role.id.value)

        mock_role_repository.delete.assert_awaited_once()

    async def test_raises_when_not_found(self, usecase, mock_role_repository):
        mock_role_repository.find_by_id.return_value = None

        with pytest.raises(RoleNotFoundException):
            await usecase.execute(uuid4())

        mock_role_repository.delete.assert_not_awaited()

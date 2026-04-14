import pytest
from uuid import uuid4

from app.modules.auth.application.usecases.role.add_permission_to_role_usecase import AddPermissionToRoleUseCase
from app.modules.auth.application.usecases.role.remove_permission_from_role_usecase import RemovePermissionFromRoleUseCase
from app.modules.auth.application.dtos.role.role_inputs import AddPermissionToRoleDTO, RemovePermissionFromRoleDTO

from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.exceptions.auth_exceptions import (
    RoleNotFoundException,
    RoleAlreadyAssignedException,
    RoleNotAssignedException,
)
from app.modules.auth.domain.exceptions.auth_exceptions import PermissionNotFoundException
from app.modules.auth.domain.value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId

def make_role(name: str, with_id: EntityId | None = None):
    return Role(
        id=with_id or EntityId(str(uuid4())),
        nome=RoleName(name),
        _permissions=[],
    )


# ============================================================================
# ADD PERMISSION TO ROLE
# ============================================================================

class TestAddPermissionToRoleUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return AddPermissionToRoleUseCase(mock_role_repository)

    async def test_adds_permission_successfully(self, usecase, mock_role_repository):
        mock_role_repository.add_permission_to_role.return_value = True

        result = await usecase.execute(
            AddPermissionToRoleDTO(role_id=uuid4(), permission_id=uuid4())
        )

        assert result is True
        mock_role_repository.add_permission_to_role.assert_awaited_once()

    async def test_raises_when_role_not_found(self, usecase, mock_role_repository):
        mock_role_repository.add_permission_to_role.side_effect = RoleNotFoundException(
            "Role não encontrada"
        )

        with pytest.raises(RoleNotFoundException):
            await usecase.execute(
                AddPermissionToRoleDTO(role_id=uuid4(), permission_id=uuid4())
            )

    async def test_raises_when_permission_not_found(self, usecase, mock_role_repository):
        mock_role_repository.add_permission_to_role.side_effect = PermissionNotFoundException(
            "Permissão não encontrada"
        )

        with pytest.raises(PermissionNotFoundException):
            await usecase.execute(
                AddPermissionToRoleDTO(role_id=uuid4(), permission_id=uuid4())
            )

    async def test_raises_when_already_assigned(self, usecase, mock_role_repository):
        mock_role_repository.add_permission_to_role.side_effect = RoleAlreadyAssignedException(
            "Permissão já associada"
        )

        with pytest.raises(RoleAlreadyAssignedException):
            await usecase.execute(
                AddPermissionToRoleDTO(role_id=uuid4(), permission_id=uuid4())
            )


# ============================================================================
# REMOVE PERMISSION FROM ROLE
# ============================================================================

class TestRemovePermissionFromRoleUseCase:

    @pytest.fixture
    def usecase(self, mock_role_repository):
        return RemovePermissionFromRoleUseCase(mock_role_repository)

    async def test_removes_permission_successfully(self, usecase, mock_role_repository):
        mock_role_repository.remove_permission_from_role.return_value = True

        result = await usecase.execute(
            RemovePermissionFromRoleDTO(role_id=uuid4(), permission_id=uuid4())
        )

        assert result is True
        mock_role_repository.remove_permission_from_role.assert_awaited_once()

    async def test_raises_when_role_not_found(self, usecase, mock_role_repository):
        mock_role_repository.remove_permission_from_role.side_effect = RoleNotFoundException(
            "Role não encontrada"
        )

        with pytest.raises(RoleNotFoundException):
            await usecase.execute(
                RemovePermissionFromRoleDTO(role_id=uuid4(), permission_id=uuid4())
            )

    async def test_raises_when_permission_not_assigned(self, usecase, mock_role_repository):
        mock_role_repository.remove_permission_from_role.side_effect = RoleNotAssignedException(
            "Permissão não está associada"
        )

        with pytest.raises(RoleNotAssignedException):
            await usecase.execute(
                RemovePermissionFromRoleDTO(role_id=uuid4(), permission_id=uuid4())
            )

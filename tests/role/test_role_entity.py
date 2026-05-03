import pytest
from unittest.mock import MagicMock
from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId


def make_permission(nome: str = "users.read") -> MagicMock:
    """Helper para criar um mock de Permission."""
    perm = MagicMock()
    perm.id = EntityId.generate()
    perm.nome = MagicMock()
    perm.nome.__eq__ = lambda self, other: other == nome
    perm.nome.value = nome
    return perm


class TestRoleCreate:

    def test_create_generates_id(self):
        role = Role.create(RoleName("admin"))
        assert role.id is not None

    def test_create_sets_name(self):
        role = Role.create(RoleName("editor"))
        assert role.nome.value == "editor"

    def test_create_starts_with_empty_permissions(self):
        role = Role.create(RoleName("admin"))
        assert role.permissions == ()

    def test_two_roles_have_different_ids(self):
        role1 = Role.create(RoleName("admin"))
        role2 = Role.create(RoleName("editor"))
        assert role1.id != role2.id


class TestRoleReconstruct:

    def test_reconstruct_preserves_id(self):
        entity_id = EntityId.generate()
        role = Role.reconstruct(
            id=entity_id,
            nome=RoleName("admin"),
            permissions=[],
        )
        assert role.id == entity_id

    def test_reconstruct_preserves_permissions(self):
        perm = make_permission("users.read")
        role = Role.reconstruct(
            id=EntityId.generate(),
            nome=RoleName("admin"),
            permissions=[perm],
        )
        assert len(role.permissions) == 1


class TestRoleUpdateName:

    def test_update_name_changes_nome(self):
        role = Role.create(RoleName("editor"))
        role.update_name(RoleName("super_editor"))
        assert role.nome.value == "super_editor"


class TestRolePermissions:

    def test_add_permission(self):
        role = Role.create(RoleName("admin"))
        perm = make_permission("users.create")
        role.add_permission(perm)
        assert len(role.permissions) == 1

    def test_add_duplicate_permission_is_ignored(self):
        role = Role.create(RoleName("admin"))
        perm = make_permission("users.create")
        role.add_permission(perm)
        role.add_permission(perm)
        assert len(role.permissions) == 1

    def test_remove_permission(self):
        role = Role.create(RoleName("admin"))
        perm = make_permission("users.delete")
        role.add_permission(perm)
        role.remove_permission(perm)
        assert len(role.permissions) == 0

    def test_remove_nonexistent_permission_does_not_raise(self):
        role = Role.create(RoleName("admin"))
        perm = make_permission("users.delete")
        role.remove_permission(perm)  # não deve lançar
        assert len(role.permissions) == 0

    def test_clear_permissions(self):
        role = Role.create(RoleName("admin"))
        role.add_permission(make_permission("users.read"))
        role.add_permission(make_permission("users.create"))
        role.clear_permissions()
        assert role.permissions == ()

    def test_permissions_returns_tuple(self):
        role = Role.create(RoleName("admin"))
        assert isinstance(role.permissions, tuple)

    def test_permissions_tuple_is_immutable(self):
        role = Role.create(RoleName("admin"))
        with pytest.raises(AttributeError):
            role.permissions.append(make_permission())  # type: ignore


class TestRoleIdentity:

    def test_two_roles_with_same_id_are_equal(self):
        entity_id = EntityId.generate()
        role1 = Role.reconstruct(id=entity_id, nome=RoleName("admin"), permissions=[])
        role2 = Role.reconstruct(id=entity_id, nome=RoleName("editor"), permissions=[])
        assert role1 == role2

    def test_two_roles_with_different_id_are_not_equal(self):
        role1 = Role.create(RoleName("admin"))
        role2 = Role.create(RoleName("admin"))
        assert role1 != role2

    def test_hash_consistent_with_equality(self):
        entity_id = EntityId.generate()
        role1 = Role.reconstruct(id=entity_id, nome=RoleName("admin"), permissions=[])
        role2 = Role.reconstruct(id=entity_id, nome=RoleName("editor"), permissions=[])
        assert hash(role1) == hash(role2)

    def test_roles_usable_in_set(self):
        entity_id = EntityId.generate()
        role1 = Role.reconstruct(id=entity_id, nome=RoleName("admin"), permissions=[])
        role2 = Role.reconstruct(id=entity_id, nome=RoleName("admin"), permissions=[])
        assert len({role1, role2}) == 1

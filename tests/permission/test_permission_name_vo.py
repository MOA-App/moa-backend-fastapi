import pytest
from app.modules.auth.domain.value_objects.permission_name_vo import PermissionName
from app.modules.auth.domain.exceptions.auth_exceptions import InvalidPermissionFormatException


class TestPermissionName:

    # -------- Criação válida --------

    def test_create_simple_permission(self):
        pn = PermissionName("users.create")
        assert pn.value == "users.create"

    def test_normalizes_to_lowercase(self):
        pn = PermissionName("USERS.CREATE")
        assert pn.value == "users.create"

    def test_strips_whitespace(self):
        pn = PermissionName("  users.read  ")
        assert pn.value == "users.read"

    def test_accepts_nested_permission(self):
        pn = PermissionName("admin.users.delete")
        assert pn.value == "admin.users.delete"

    def test_accepts_max_depth_5(self):
        pn = PermissionName("a.b.c.d.e")
        assert pn.get_depth() == 5

    def test_accepts_underscores_in_parts(self):
        pn = PermissionName("admin_panel.bulk_delete")
        assert pn.value == "admin_panel.bulk_delete"

    def test_accepts_numbers_in_parts(self):
        pn = PermissionName("tier1.read")
        assert pn.value == "tier1.read"

    def test_immutability(self):
        pn = PermissionName("users.read")
        with pytest.raises(Exception):
            pn.value = "hacked"

    # -------- Propriedades --------

    def test_action_returns_last_part(self):
        pn = PermissionName("users.create")
        assert pn.action == "create"

    def test_action_nested_returns_last_part(self):
        pn = PermissionName("admin.users.delete")
        assert pn.action == "delete"

    def test_resource_returns_permission_resource_vo(self):
        from app.modules.auth.domain.value_objects.permission_resource_vo import PermissionResource
        pn = PermissionName("users.create")
        assert isinstance(pn.resource, PermissionResource)
        assert pn.resource.value == "users"

    def test_get_base_resource_simple(self):
        pn = PermissionName("users.create")
        assert pn.get_base_resource() == "users"

    def test_get_base_resource_nested(self):
        pn = PermissionName("admin.users.delete")
        assert pn.get_base_resource() == "admin"

    def test_get_parts(self):
        pn = PermissionName("admin.users.delete")
        assert pn.get_parts() == ["admin", "users", "delete"]

    def test_get_depth_simple(self):
        pn = PermissionName("users.create")
        assert pn.get_depth() == 2

    def test_get_depth_nested(self):
        pn = PermissionName("admin.users.delete")
        assert pn.get_depth() == 3

    def test_is_nested_false_for_simple(self):
        pn = PermissionName("users.create")
        assert pn.is_nested() is False

    def test_is_nested_true_for_deep(self):
        pn = PermissionName("admin.users.delete")
        assert pn.is_nested() is True

    def test_str_returns_value(self):
        pn = PermissionName("users.read")
        assert str(pn) == "users.read"

    def test_equality(self):
        assert PermissionName("users.read") == PermissionName("users.read")

    def test_inequality(self):
        assert PermissionName("users.read") != PermissionName("users.create")

    # -------- Validações inválidas --------

    def test_raises_on_empty(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("")

    def test_raises_on_too_short(self):
        with pytest.raises(InvalidPermissionFormatException, match="muito curto"):
            PermissionName("ab")

    def test_raises_on_too_long(self):
        with pytest.raises(InvalidPermissionFormatException, match="muito longo"):
            PermissionName("a" * 101)

    def test_raises_without_dot(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("usersread")

    def test_raises_on_single_part(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("users")

    def test_raises_on_depth_greater_than_5(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("a.b.c.d.e.f")

    def test_raises_on_special_characters(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("users.create!")

    def test_raises_on_uppercase_after_normalization_attempt(self):
        # Mesmo com letras maiúsculas, deve normalizar e passar — já testado acima
        # Aqui testamos caracteres inválidos mesmo após lowercase
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("users.créate")

    def test_raises_on_empty_part(self):
        with pytest.raises(InvalidPermissionFormatException):
            PermissionName("users..create")

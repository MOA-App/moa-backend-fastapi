import pytest
from app.modules.auth.domain.value_objects.permission_resource_vo import PermissionResource


class TestPermissionResource:

    # -------- Criação válida --------

    def test_create_valid_resource(self):
        r = PermissionResource("users")
        assert r.value == "users"

    def test_accepts_numbers_in_name(self):
        r = PermissionResource("tier1")
        assert r.value == "tier1"

    def test_accepts_underscore(self):
        r = PermissionResource("admin_panel")
        assert r.value == "admin_panel"

    def test_str_returns_value(self):
        r = PermissionResource("posts")
        assert str(r) == "posts"

    def test_equality(self):
        assert PermissionResource("users") == PermissionResource("users")

    def test_inequality(self):
        assert PermissionResource("users") != PermissionResource("posts")

    def test_usable_as_dict_key(self):
        d = {PermissionResource("users"): 1}
        assert d[PermissionResource("users")] == 1

    # -------- Validações inválidas --------

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError, match="não pode ser vazio"):
            PermissionResource("")

    def test_raises_on_uppercase(self):
        with pytest.raises(ValueError):
            PermissionResource("Users")

    def test_raises_starting_with_number(self):
        with pytest.raises(ValueError):
            PermissionResource("1users")

    def test_raises_on_hyphen(self):
        with pytest.raises(ValueError):
            PermissionResource("admin-panel")

    def test_raises_on_dot(self):
        with pytest.raises(ValueError):
            PermissionResource("admin.panel")

    def test_raises_on_space(self):
        with pytest.raises(ValueError):
            PermissionResource("admin panel")

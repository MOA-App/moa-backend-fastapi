import pytest
from app.modules.auth.domain.value_objects.role_name_vo import RoleName


class TestRoleName:

    # -------- Criação válida --------

    def test_create_valid_name(self):
        role_name = RoleName("admin")
        assert role_name.value == "admin"

    def test_normalizes_to_lowercase(self):
        role_name = RoleName("ADMIN")
        assert role_name.value == "admin"

    def test_strips_whitespace(self):
        role_name = RoleName("  editor  ")
        assert role_name.value == "editor"

    def test_accepts_underscores(self):
        role_name = RoleName("super_admin")
        assert role_name.value == "super_admin"

    def test_accepts_numbers(self):
        role_name = RoleName("tier1_support")
        assert role_name.value == "tier1_support"

    def test_accepts_exactly_2_chars(self):
        role_name = RoleName("hr")
        assert role_name.value == "hr"

    def test_accepts_exactly_100_chars(self):
        role_name = RoleName("a" * 100)
        assert len(role_name.value) == 100

    def test_str_returns_value(self):
        role_name = RoleName("admin")
        assert str(role_name) == "admin"

    def test_equality(self):
        assert RoleName("admin") == RoleName("admin")

    def test_inequality(self):
        assert RoleName("admin") != RoleName("editor")

    # -------- Validações inválidas --------

    def test_raises_on_empty_string(self):
        with pytest.raises(ValueError, match="não pode ser vazio"):
            RoleName("")

    def test_raises_on_whitespace_only(self):
        with pytest.raises(ValueError):
            RoleName("   ")

    def test_raises_on_less_than_2_chars(self):
        with pytest.raises(ValueError, match="mínimo 2 caracteres"):
            RoleName("a")

    def test_raises_on_more_than_100_chars(self):
        with pytest.raises(ValueError, match="máximo 100 caracteres"):
            RoleName("a" * 101)

    def test_raises_on_special_characters(self):
        with pytest.raises(ValueError, match="apenas letras"):
            RoleName("admin!")

    def test_raises_on_spaces_in_name(self):
        with pytest.raises(ValueError, match="apenas letras"):
            RoleName("super admin")

    def test_raises_on_hyphen(self):
        with pytest.raises(ValueError, match="apenas letras"):
            RoleName("super-admin")

    def test_immutability(self):
        role_name = RoleName("admin")
        with pytest.raises(Exception):
            role_name.value = "hacked"

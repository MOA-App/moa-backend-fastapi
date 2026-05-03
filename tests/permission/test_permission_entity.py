import pytest
from datetime import datetime, timezone
from app.modules.auth.domain.entities.permission_entity import Permission
from app.modules.auth.domain.value_objects.permission_name_vo import PermissionName
from app.modules.auth.domain.value_objects.permission_resource_vo import PermissionResource
from app.shared.domain.value_objects.id_vo import EntityId


def make_permission(nome="users.create", descricao=None, with_id=None):
    if with_id:
        return Permission.reconstruct(
            id=with_id,
            nome=PermissionName(nome),
            descricao=descricao,
            data_criacao=datetime.now(timezone.utc),
        )
    return Permission.create(
        nome=PermissionName(nome),
        descricao=descricao,
    )

class TestPermissionCreate:

    def test_create_generates_id(self):
        p = make_permission()
        assert p.id is not None

    def test_create_sets_nome(self):
        p = make_permission("users.read")
        assert p.nome.value == "users.read"

    def test_create_sets_descricao(self):
        p = make_permission(descricao="Leitura de usuários")
        assert p.descricao == "Leitura de usuários"

    def test_create_descricao_none_by_default(self):
        p = make_permission()
        assert p.descricao is None

    def test_create_sets_data_criacao(self):
        p = make_permission()
        assert isinstance(p.data_criacao, datetime)
        assert p.data_criacao.tzinfo is not None

    def test_two_permissions_have_different_ids(self):
        p1 = make_permission()
        p2 = make_permission()
        assert p1.id != p2.id


class TestPermissionReconstruct:

    def test_reconstruct_preserves_id(self):
        entity_id = EntityId.generate()
        p = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("users.read"),
            descricao=None,
            data_criacao=datetime.now(timezone.utc),
        )
        assert p.id == entity_id

    def test_reconstruct_preserves_all_fields(self):
        entity_id = EntityId.generate()
        dt = datetime.now(timezone.utc)
        p = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("posts.delete"),
            descricao="Deletar posts",
            data_criacao=dt,
        )
        assert p.nome.value == "posts.delete"
        assert p.descricao == "Deletar posts"
        assert p.data_criacao == dt


class TestPermissionUpdateDescription:

    def test_returns_new_instance(self):
        p = make_permission()
        p2 = p.update_description("Nova descrição")
        assert p is not p2

    def test_new_instance_has_updated_description(self):
        p = make_permission()
        p2 = p.update_description("Nova descrição")
        assert p2.descricao == "Nova descrição"

    def test_original_is_unchanged(self):
        p = make_permission(descricao="Original")
        p.update_description("Modificada")
        assert p.descricao == "Original"

    def test_update_to_none(self):
        p = make_permission(descricao="Alguma descrição")
        p2 = p.update_description(None)
        assert p2.descricao is None


class TestPermissionBehavior:

    def test_is_for_resource_true(self):
        p = make_permission("users.create")
        assert p.is_for_resource(PermissionResource("users")) is True

    def test_is_for_resource_false(self):
        p = make_permission("users.create")
        assert p.is_for_resource(PermissionResource("posts")) is False

    def test_is_action_true(self):
        p = make_permission("users.create")
        assert p.is_action("create") is True

    def test_is_action_false(self):
        p = make_permission("users.create")
        assert p.is_action("delete") is False

    def test_is_action_case_insensitive(self):
        p = make_permission("users.create")
        assert p.is_action("CREATE") is True

    def test_resource_returns_base(self):
        p = make_permission("users.create")
        assert p.resource() == "users"

    def test_action_returns_last_part(self):
        p = make_permission("admin.users.delete")
        assert p.action() == "delete"

    def test_get_full_name(self):
        p = make_permission("users.create")
        assert p.get_full_name() == "users.create"


class TestPermissionMatches:

    def test_exact_match(self):
        p = make_permission("users.create")
        assert p.matches("users.create") is True

    def test_exact_no_match(self):
        p = make_permission("users.create")
        assert p.matches("users.delete") is False

    def test_wildcard_action(self):
        p = make_permission("users.create")
        assert p.matches("users.*") is True

    def test_wildcard_action_no_match_other_resource(self):
        p = make_permission("users.create")
        assert p.matches("posts.*") is False

    def test_wildcard_resource(self):
        p = make_permission("users.create")
        assert p.matches("*.create") is True

    def test_wildcard_resource_no_match_other_action(self):
        p = make_permission("users.create")
        assert p.matches("*.delete") is False

    def test_full_wildcard(self):
        p = make_permission("users.create")
        assert p.matches("*.*") is True

    def test_case_insensitive_pattern(self):
        p = make_permission("users.create")
        assert p.matches("USERS.CREATE") is True


class TestPermissionIdentity:

    def test_same_id_equal(self):
        entity_id = EntityId.generate()
        p1 = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("users.read"),
            descricao=None,
            data_criacao=datetime.now(timezone.utc),
        )
        p2 = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("users.create"),
            descricao="Outra",
            data_criacao=datetime.now(timezone.utc),
        )
        assert p1 == p2

    def test_different_id_not_equal(self):
        p1 = make_permission("users.read")
        p2 = make_permission("users.read")
        assert p1 != p2

    def test_hash_consistent_with_equality(self):
        entity_id = EntityId.generate()
        p1 = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("users.read"),
            descricao=None,
            data_criacao=datetime.now(timezone.utc),
        )
        p2 = Permission.reconstruct(
            id=entity_id,
            nome=PermissionName("users.create"),
            descricao=None,
            data_criacao=datetime.now(timezone.utc),
        )
        assert hash(p1) == hash(p2)

    def test_usable_in_set(self):
        entity_id = EntityId.generate()
        dt = datetime.now(timezone.utc)
        p1 = Permission.reconstruct(
            id=entity_id, nome=PermissionName("users.read"),
            descricao=None, data_criacao=dt,
        )
        p2 = Permission.reconstruct(
            id=entity_id, nome=PermissionName("users.read"),
            descricao=None, data_criacao=dt,
        )
        assert len({p1, p2}) == 1

    def test_str_representation(self):
        p = make_permission("users.create")
        assert "users.create" in str(p)

    def test_immutability(self):
        p = make_permission()
        with pytest.raises(Exception):
            p.nome = PermissionName("posts.delete")

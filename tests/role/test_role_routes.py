import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from app.modules.auth.domain.exceptions.auth_exceptions import (
    RoleNotFoundException,
    RoleAlreadyExistsException,
    RoleAlreadyAssignedException,
    RoleNotAssignedException,
)

# ── helpers ──────────────────────────────────────────────────────────────────

ROLE_ID = str(uuid4())
PERMISSION_ID = str(uuid4())

ROLE_RESPONSE = {
    "id": ROLE_ID,
    "nome": "admin",
    "permissions": [],
    "data_criacao": "2024-01-15T10:30:00+00:00",
}


# ── fixtures ─────────────────────────────────────────────────────────────────

@pytest.fixture
async def client(app):
    async def fake_permission():
        return None

    from app.modules.auth.presentation.dependencies.permissions import require_permission
    from app.modules.auth.presentation.dependencies.role import (
        get_create_role_usecase,
        get_role_by_id_usecase,
        get_list_roles_usecase,
        get_update_role_usecase,
        get_delete_role_usecase,
        get_add_permission_to_role_usecase,
        get_remove_permission_from_role_usecase,
    )

    # mocks dos usecases
    create_uc = AsyncMock()
    get_uc = AsyncMock()
    list_uc = AsyncMock()
    update_uc = AsyncMock()
    delete_uc = AsyncMock()
    add_perm_uc = AsyncMock()
    remove_perm_uc = AsyncMock()

    app.dependency_overrides = {
        # override de permissões (CORRETO)
        require_permission: lambda *args, **kwargs: fake_permission,

        # override dos usecases
        get_create_role_usecase: lambda: create_uc,
        get_role_by_id_usecase: lambda: get_uc,
        get_list_roles_usecase: lambda: list_uc,
        get_update_role_usecase: lambda: update_uc,
        get_delete_role_usecase: lambda: delete_uc,
        get_add_permission_to_role_usecase: lambda: add_perm_uc,
        get_remove_permission_from_role_usecase: lambda: remove_perm_uc,
    }

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        # expõe os mocks para os testes
        c.create_uc = create_uc
        c.get_uc = get_uc
        c.list_uc = list_uc
        c.update_uc = update_uc
        c.delete_uc = delete_uc
        c.add_perm_uc = add_perm_uc
        c.remove_perm_uc = remove_perm_uc
        yield c

    app.dependency_overrides = {}


# ── POST /roles ───────────────────────────────────────────────────────────────

class TestCreateRole:

    async def test_creates_role_returns_201(self, client):
        client.create_uc.execute.return_value = ROLE_RESPONSE

        response = await client.post("/roles/", json={"nome": "admin"})

        assert response.status_code == 201
        assert response.json()["success"] is True

    async def test_returns_409_when_already_exists(self, client):
        client.create_uc.execute.side_effect = RoleAlreadyExistsException("Role já existe")

        response = await client.post("/roles/", json={"nome": "admin"})

        assert response.status_code == 409
        assert response.json()["success"] is False

    async def test_returns_400_on_invalid_name(self, client):
        response = await client.post("/roles/", json={"nome": "invalid name!"})
        assert response.status_code == 400

    async def test_returns_400_on_empty_name(self, client):
        response = await client.post("/roles/", json={"nome": ""})
        assert response.status_code == 400


# ── GET /roles ────────────────────────────────────────────────────────────────

class TestListRoles:

    async def test_lists_roles_returns_200(self, client):
        client.list_uc.execute.return_value = {"roles": [ROLE_RESPONSE], "total": 1}

        response = await client.get("/roles/")

        assert response.status_code == 200
        assert response.json()["success"] is True

    async def test_returns_empty_list(self, client):
        client.list_uc.execute.return_value = {"roles": [], "total": 0}

        response = await client.get("/roles/")

        assert response.status_code == 200


# ── GET /roles/{id} ───────────────────────────────────────────────────────────

class TestGetRole:

    async def test_returns_role_when_found(self, client):
        client.get_uc.execute.return_value = ROLE_RESPONSE

        response = await client.get(f"/roles/{ROLE_ID}")

        assert response.status_code == 200

    async def test_returns_404_when_not_found(self, client):
        client.get_uc.execute.side_effect = RoleNotFoundException("Role não encontrada")

        response = await client.get(f"/roles/{ROLE_ID}")

        assert response.status_code == 404
        assert response.json()["success"] is False

    async def test_returns_422_on_invalid_uuid(self, client):
        response = await client.get("/roles/not-a-uuid")

        # pode ser 400 dependendo da sua config
        assert response.status_code in (400, 422)


# ── PUT /roles/{id} ───────────────────────────────────────────────────────────

class TestUpdateRole:

    async def test_updates_role_returns_200(self, client):
        client.update_uc.execute.return_value = {**ROLE_RESPONSE, "nome": "super_admin"}

        response = await client.put(f"/roles/{ROLE_ID}", json={"nome": "super_admin"})

        assert response.status_code == 200

    async def test_returns_404_when_not_found(self, client):
        client.update_uc.execute.side_effect = RoleNotFoundException("Role não encontrada")

        response = await client.put(f"/roles/{ROLE_ID}", json={"nome": "new_name"})

        assert response.status_code == 404

    async def test_returns_409_when_name_conflict(self, client):
        client.update_uc.execute.side_effect = RoleAlreadyExistsException("Nome já existe")

        response = await client.put(f"/roles/{ROLE_ID}", json={"nome": "admin"})

        assert response.status_code == 409


# ── DELETE /roles/{id} ────────────────────────────────────────────────────────

class TestDeleteRole:

    async def test_deletes_role_returns_204(self, client):
        client.delete_uc.execute.return_value = None

        response = await client.delete(f"/roles/{ROLE_ID}")

        assert response.status_code == 204

    async def test_returns_404_when_not_found(self, client):
        client.delete_uc.execute.side_effect = RoleNotFoundException("Role não encontrada")

        response = await client.delete(f"/roles/{ROLE_ID}")

        assert response.status_code == 404


# ── POST /roles/{id}/permissions ─────────────────────────────────────────────

class TestAddPermissionToRole:

    async def test_adds_permission_returns_200(self, client):
        client.add_perm_uc.execute.return_value = True

        response = await client.post(
            f"/roles/{ROLE_ID}/permissions",
            json={"permission_id": PERMISSION_ID},
        )

        assert response.status_code == 200

    async def test_returns_409_when_already_assigned(self, client):
        client.add_perm_uc.execute.side_effect = RoleAlreadyAssignedException("Já associada")

        response = await client.post(
            f"/roles/{ROLE_ID}/permissions",
            json={"permission_id": PERMISSION_ID},
        )

        assert response.status_code == 409

    async def test_returns_404_when_role_not_found(self, client):
        client.add_perm_uc.execute.side_effect = RoleNotFoundException("Role não encontrada")

        response = await client.post(
            f"/roles/{ROLE_ID}/permissions",
            json={"permission_id": PERMISSION_ID},
        )

        assert response.status_code == 404


# ── DELETE /roles/{id}/permissions/{perm_id} ─────────────────────────────────

class TestRemovePermissionFromRole:

    async def test_removes_permission_returns_204(self, client):
        client.remove_perm_uc.execute.return_value = True

        response = await client.delete(f"/roles/{ROLE_ID}/permissions/{PERMISSION_ID}")

        assert response.status_code == 204

    async def test_returns_400_when_not_assigned(self, client):
        client.remove_perm_uc.execute.side_effect = RoleNotAssignedException("Permissão não associada")

        response = await client.delete(f"/roles/{ROLE_ID}/permissions/{PERMISSION_ID}")

        assert response.status_code == 400

    async def test_returns_404_when_role_not_found(self, client):
        client.remove_perm_uc.execute.side_effect = RoleNotFoundException("Role não encontrada")

        response = await client.delete(f"/roles/{ROLE_ID}/permissions/{PERMISSION_ID}")

        assert response.status_code == 404

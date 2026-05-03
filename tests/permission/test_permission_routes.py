import pytest
from uuid import uuid4
from unittest.mock import AsyncMock
from httpx import AsyncClient, ASGITransport

from app.modules.auth.presentation.routes.permission_routes import (
    get_create_permission_usecase,
    get_list_permissions_usecase,
    get_permission_usecase,
    get_update_permission_usecase,
    get_delete_permission_usecase,
    get_bulk_create_permissions_usecase,
    get_list_resources_usecase,
)

PERMISSION_ID = str(uuid4())

PERMISSION_RESPONSE = {
    "id": PERMISSION_ID,
    "nome": "users.create",
}


@pytest.fixture
async def client(app):
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


# ================= CREATE =================

async def test_create_permission(client, app):
    uc = AsyncMock()
    uc.execute.return_value = PERMISSION_RESPONSE

    app.dependency_overrides[get_create_permission_usecase] = lambda: uc

    response = await client.post(
        "/permissions",
        json={"nome": "users.create"},
    )

    assert response.status_code == 201
    assert response.json()["success"] is True


# ================= LIST =================

async def test_list_permissions(client, app):
    uc = AsyncMock()
    uc.execute.return_value = [PERMISSION_RESPONSE]

    app.dependency_overrides[get_list_permissions_usecase] = lambda: uc

    response = await client.get("/permissions")

    assert response.status_code == 200
    assert response.json()["success"] is True


# ================= GET =================

async def test_get_permission(client, app):
    uc = AsyncMock()
    uc.execute.return_value = PERMISSION_RESPONSE

    app.dependency_overrides[get_permission_usecase] = lambda: uc

    response = await client.get(f"/permissions/{PERMISSION_ID}")

    assert response.status_code == 200


# ================= UPDATE =================

async def test_update_permission(client, app):
    uc = AsyncMock()
    uc.execute.return_value = PERMISSION_RESPONSE

    app.dependency_overrides[get_update_permission_usecase] = lambda: uc

    response = await client.put(
        f"/permissions/{PERMISSION_ID}",
        json={"descricao": "Nova"},
    )

    assert response.status_code == 200


# ================= DELETE =================

async def test_delete_permission(client, app):
    uc = AsyncMock()
    uc.execute.return_value = None

    app.dependency_overrides[get_delete_permission_usecase] = lambda: uc

    response = await client.delete(f"/permissions/{PERMISSION_ID}")

    assert response.status_code == 204


# ================= BULK =================

async def test_bulk_create(client, app):
    uc = AsyncMock()
    uc.execute.return_value = {"created": [PERMISSION_RESPONSE]}

    app.dependency_overrides[get_bulk_create_permissions_usecase] = lambda: uc

    response = await client.post(
        "/permissions/bulk",
        json={"permissions": [{"nome": "users.create"}]},
    )

    assert response.status_code == 201


# ================= RESOURCES =================

async def test_list_resources(client, app):
    uc = AsyncMock()
    uc.execute.return_value = ["users"]

    app.dependency_overrides[get_list_resources_usecase] = lambda: uc

    response = await client.get("/permissions/resources/list")

    assert response.status_code == 200
    assert response.json()["data"] == ["users"]

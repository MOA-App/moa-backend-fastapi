import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.modules.auth.domain.exceptions.auth_exceptions import (
    PermissionNotFoundException,
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.modules.auth.setup import setup_auth_module


@pytest.fixture
def auth_app() -> FastAPI:
    app = FastAPI()
    setup_auth_module(app)

    @app.get("/test/user-not-found")
    async def user_not_found():
        raise UserNotFoundException("Usuário não encontrado")

    @app.get("/test/user-already-exists")
    async def user_already_exists():
        raise UserAlreadyExistsException("Usuário já existe")

    @app.get("/test/permission-not-found")
    async def permission_not_found():
        raise PermissionNotFoundException("Permissão não encontrada")

    return app


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("path", "expected_status"),
    [
        ("/test/user-not-found", 404),
        ("/test/user-already-exists", 409),
        ("/test/permission-not-found", 404),
    ],
)
async def test_auth_domain_errors_have_expected_http_status(
    auth_app: FastAPI,
    path: str,
    expected_status: int,
):
    async with AsyncClient(
        transport=ASGITransport(app=auth_app), base_url="http://test"
    ) as client:
        response = await client.get(path)

    assert response.status_code == expected_status
    assert response.json()["success"] is False

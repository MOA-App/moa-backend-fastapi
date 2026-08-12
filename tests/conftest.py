import pytest
from unittest.mock import AsyncMock

from app.main import app as fastapi_app
from app.core.config import settings
from app.shared.presentation.middlewares.rate_limit_middleware import InMemoryRateLimiter


# ============================
# APP FIXTURE
# ============================

@pytest.fixture
def app():
    return fastapi_app


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Evita que o estado em memória de um teste afete os demais."""
    fastapi_app.state.rate_limiter = InMemoryRateLimiter(
        max_requests=settings.RATE_LIMIT_REQUESTS,
        window_seconds=settings.RATE_LIMIT_WINDOW_SECONDS,
    )


# ============================
# PERMISSION REPOSITORY
# ============================

@pytest.fixture
def mock_permission_repository():
    repo = AsyncMock()

    repo.create = AsyncMock()
    repo.exists_by_name = AsyncMock(return_value=False)
    repo.find_by_id = AsyncMock()
    repo.list_all = AsyncMock()
    repo.list_resources = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()

    return repo


# ============================
# ROLE REPOSITORY
# ============================

@pytest.fixture
def mock_role_repository():
    repo = AsyncMock()

    repo.create = AsyncMock()
    repo.exists_by_name = AsyncMock(return_value=False)
    repo.find_by_id = AsyncMock()
    repo.find_by_name = AsyncMock()
    repo.list_all = AsyncMock()
    repo.update = AsyncMock()
    repo.delete = AsyncMock()

    return repo

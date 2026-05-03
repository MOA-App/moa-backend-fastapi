import pytest
from unittest.mock import AsyncMock


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

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.shared.presentation.middlewares.rate_limit_middleware import InMemoryRateLimiter


@pytest.fixture(autouse=True)
async def rate_limiter():
    original = app.state.rate_limiter
    app.state.rate_limiter = InMemoryRateLimiter(max_requests=2, window_seconds=60)
    yield
    app.state.rate_limiter = original


@pytest.mark.asyncio
async def test_blocks_requests_after_the_configured_limit():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        first = await client.get("/")
        second = await client.get("/")
        blocked = await client.get("/")

    assert first.status_code == 200
    assert first.headers["X-RateLimit-Limit"] == "2"
    assert first.headers["X-RateLimit-Remaining"] == "1"
    assert second.headers["X-RateLimit-Remaining"] == "0"
    assert blocked.status_code == 429
    assert blocked.json()["success"] is False
    assert blocked.headers["Retry-After"]


@pytest.mark.asyncio
async def test_limits_are_independent_per_client_ip():
    async with AsyncClient(
        transport=ASGITransport(app=app, client=("198.51.100.1", 50000)),
        base_url="http://test",
    ) as client:
        await client.get("/")
        await client.get("/")
        blocked = await client.get("/")

    async with AsyncClient(
        transport=ASGITransport(app=app, client=("198.51.100.2", 50000)),
        base_url="http://test",
    ) as client:
        other_client = await client.get("/")

    assert blocked.status_code == 429
    assert other_client.status_code == 200


@pytest.mark.asyncio
async def test_health_and_options_are_not_limited():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        for _ in range(3):
            response = await client.get("/health")
            assert response.status_code == 200

        response = await client.options("/")

    assert response.status_code in {200, 405}

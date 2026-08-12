"""Rate limiting em memória para proteger a API de abuso por cliente."""

from __future__ import annotations

from collections import defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
import asyncio
import math
import time

from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


@dataclass(frozen=True)
class RateLimitResult:
    allowed: bool
    remaining: int
    retry_after: int


class InMemoryRateLimiter:
    """Limitador de janela deslizante, seguro para concorrência assíncrona.

    O armazenamento é local ao processo. Para múltiplas réplicas da API, este
    componente deve ser substituído por uma implementação compartilhada (Redis).
    """

    def __init__(self, max_requests: int, window_seconds: int) -> None:
        if max_requests < 1:
            raise ValueError("max_requests deve ser maior que zero")
        if window_seconds < 1:
            raise ValueError("window_seconds deve ser maior que zero")

        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, deque[float]] = defaultdict(deque)
        self._lock = asyncio.Lock()

    async def check(self, key: str) -> RateLimitResult:
        now = time.monotonic()
        cutoff = now - self.window_seconds

        async with self._lock:
            timestamps = self._requests[key]
            while timestamps and timestamps[0] <= cutoff:
                timestamps.popleft()

            if len(timestamps) >= self.max_requests:
                retry_after = max(1, math.ceil(timestamps[0] + self.window_seconds - now))
                return RateLimitResult(False, 0, retry_after)

            timestamps.append(now)
            return RateLimitResult(True, self.max_requests - len(timestamps), 0)

    async def reset(self) -> None:
        """Limpa os contadores; útil em testes e na administração da aplicação."""
        async with self._lock:
            self._requests.clear()


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Aplica o limite por IP e adiciona cabeçalhos de rate limiting."""

    _EXCLUDED_PATHS = {"/health", "/docs", "/redoc", "/openapi.json"}

    def __init__(self, app: ASGIApp, max_requests: int, window_seconds: int) -> None:
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS" or request.url.path in self._EXCLUDED_PATHS:
            return await call_next(request)

        client_ip = self._get_client_ip(request)
        limiter = request.app.state.rate_limiter
        result = await limiter.check(client_ip)
        reset_at = datetime.now(timezone.utc).timestamp() + (
            result.retry_after or self.window_seconds
        )

        headers = {
            "X-RateLimit-Limit": str(limiter.max_requests),
            "X-RateLimit-Remaining": str(result.remaining),
            "X-RateLimit-Reset": str(math.ceil(reset_at)),
        }
        if not result.allowed:
            headers["Retry-After"] = str(result.retry_after)
            return JSONResponse(
                status_code=429,
                content={
                    "success": False,
                    "error": "Rate limit exceeded. Try again later.",
                    "retry_after": result.retry_after,
                },
                headers=headers,
            )

        response = await call_next(request)
        response.headers.update(headers)
        return response

    @staticmethod
    def _get_client_ip(request: Request) -> str:
        return request.client.host if request.client else "unknown"

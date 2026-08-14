from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from jwt import InvalidTokenError

from app.core.config import settings


class JWTHandler:
    """Creates and validates access tokens for authenticated users."""

    def create_access_token(self, subject: str) -> str:
        expires_at = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        return jwt.encode(
            {"sub": subject, "exp": expires_at, "type": "access"},
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM,
        )

    def decode_access_token(self, token: str) -> dict[str, Any]:
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=[settings.ALGORITHM],
            )
        except InvalidTokenError as exc:
            raise ValueError("Token de acesso invalido ou expirado.") from exc

        if payload.get("type") != "access" or not isinstance(payload.get("sub"), str):
            raise ValueError("Token de acesso invalido.")

        return payload

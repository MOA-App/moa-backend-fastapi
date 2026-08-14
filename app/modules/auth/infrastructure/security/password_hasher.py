import bcrypt

from app.core.config import settings
from app.modules.auth.domain.services.password_hasher_interface import PasswordHasherInterface


class PasswordHasher(PasswordHasherInterface):
    """Password hashing service used by the auth use cases."""

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(
            password.encode("utf-8"),
            bcrypt.gensalt(rounds=settings.BCRYPT_ROUNDS),
        ).decode("utf-8")

    def verify(self, password: str, hashed_password: str) -> bool:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                hashed_password.encode("utf-8"),
            )
        except (ValueError, TypeError):
            return False

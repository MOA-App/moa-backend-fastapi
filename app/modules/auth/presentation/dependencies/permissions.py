from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.modules.auth.domain.entities.user_entity import User
from app.modules.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.shared.domain.value_objects.id_vo import EntityId

from .user import get_user_repository


_bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: Annotated[
        HTTPAuthorizationCredentials | None, Depends(_bearer_scheme)
    ],
    user_repository: Annotated[UserRepositoryImpl, Depends(get_user_repository)],
) -> User:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de acesso ausentes.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        payload = JWTHandler().decode_access_token(credentials.credentials)
        user_id = EntityId.from_string(payload["sub"])
    except (KeyError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token de acesso invalido ou expirado.",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    user = await user_repository.get_by_id(user_id)
    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario nao encontrado ou inativo.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


def require_permission(permission: str):
    normalized_permission = permission.replace(":", ".").lower()

    async def dependency(
        current_user: Annotated[User, Depends(get_current_user)],
    ) -> User:
        if not current_user.has_permission(normalized_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario nao possui a permissao necessaria.",
            )
        return current_user

    return dependency

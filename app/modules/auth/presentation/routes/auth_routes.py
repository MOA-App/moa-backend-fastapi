from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from app.modules.auth.infrastructure.security.password_hasher import PasswordHasher
from app.modules.auth.presentation.dependencies.user import get_user_repository
from app.modules.auth.presentation.schemas.user.user_request import LoginRequest


router = APIRouter(prefix="/auth", tags=["Authentication"])


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=AccessTokenResponse)
async def login(
    request: LoginRequest,
    user_repository: UserRepositoryImpl = Depends(get_user_repository),
):
    user = await user_repository.get_by_email(Email(str(request.email)))
    if (
        user is None
        or not user.is_active
        or not PasswordHasher().verify(request.password, user.password.value)
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha invalidos.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return AccessTokenResponse(
        access_token=JWTHandler().create_access_token(str(user.id.value))
    )

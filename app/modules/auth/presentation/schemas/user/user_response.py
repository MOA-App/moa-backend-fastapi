from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class UserResponse(BaseModel):
    """
    Resposta padrão de usuário.
    """

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    email: str
    is_active: bool
    created_at: datetime
    roles: list[str] = []


class UserListResponse(BaseModel):
    """
    Lista de usuários.
    """

    users: list[UserResponse]

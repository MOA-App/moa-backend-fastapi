from dataclasses import dataclass
from datetime import datetime
from typing import List


@dataclass(frozen=True)
class UserResponse:
    """
    DTO de resposta contendo todos os dados do usuário.
    """

    id: str
    name: str
    email: str
    is_active: bool
    roles: List[str]
    created_at: datetime

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class UpdateUserRequest:
    """
    DTO utilizado para atualização de um usuário.
    Todos os campos são opcionais.
    """

    name: Optional[str] = None
    email: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None

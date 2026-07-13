from dataclasses import dataclass


@dataclass(frozen=True)
class CreateUserRequest:
    """
    DTO utilizado para criação de um usuário.
    """

    name: str
    email: str
    password: str

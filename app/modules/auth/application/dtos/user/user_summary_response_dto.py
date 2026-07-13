from dataclasses import dataclass


@dataclass(frozen=True)
class UserSummaryResponse:
    """
    DTO resumido para listagem de usuários.
    """

    id: str
    name: str
    email: str
    is_active: bool

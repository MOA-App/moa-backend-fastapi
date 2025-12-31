from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Username:
    """Value Object para Nome de Usuário"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome de usuário não pode ser vazio")

        normalized = self.value.strip().lower()

        if len(normalized) < 3:
            raise ValueError("Nome de usuário deve ter no mínimo 3 caracteres")

        if len(normalized) > 50:
            raise ValueError("Nome de usuário deve ter no máximo 50 caracteres")

        if not self._is_valid_username(normalized):
            raise ValueError(
                "Nome de usuário deve conter apenas letras, números, "
                "underscores e hífens"
            )

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_username(username: str) -> bool:
        return re.match(r"^[a-z0-9_-]+$", username) is not None

    def __str__(self) -> str:
        return self.value

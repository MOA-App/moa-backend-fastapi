from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RoleName:
    """Value Object para Nome de Role"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome da role não pode ser vazio")

        normalized = self.value.strip().lower()

        if len(normalized) < 2:
            raise ValueError("Nome da role deve ter no mínimo 2 caracteres")

        if len(normalized) > 100:
            raise ValueError("Nome da role deve ter no máximo 100 caracteres")

        if not self._is_valid_role_name(normalized):
            raise ValueError(
                "Nome da role deve conter apenas letras, números e underscores"
            )

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_role_name(name: str) -> bool:
        return re.match(r"^[a-z0-9_]+$", name) is not None

    def __str__(self) -> str:
        return self.value

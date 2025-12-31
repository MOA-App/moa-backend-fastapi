from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    """Value Object para Email"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Email não pode ser vazio")

        normalized = self.value.strip().lower()

        if not self._is_valid_email(normalized):
            raise ValueError(f"Email inválido: {self.value}")

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
        return re.match(pattern, email) is not None

    def __str__(self) -> str:
        return self.value

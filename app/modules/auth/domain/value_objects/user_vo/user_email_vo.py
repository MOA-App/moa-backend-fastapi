from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Email:
    """
    Value Object que representa um e-mail válido.
    """

    value: str

    EMAIL_REGEX = re.compile(
        r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    )

    def __post_init__(self):
        email = self.value.strip().lower()

        if not email:
            raise ValueError("E-mail não pode ser vazio.")

        if not self.EMAIL_REGEX.match(email):
            raise ValueError("E-mail inválido.")

        object.__setattr__(self, "value", email)

    def __str__(self) -> str:
        return self.value

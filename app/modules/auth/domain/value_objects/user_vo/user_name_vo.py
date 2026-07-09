from dataclasses import dataclass


@dataclass(frozen=True)
class UserName:
    """
    Value Object que representa o nome do usuário.
    """

    value: str

    MIN_LENGTH = 2
    MAX_LENGTH = 120

    def __post_init__(self):
        name = self.value.strip()

        if not name:
            raise ValueError("Nome não pode ser vazio.")

        if len(name) < self.MIN_LENGTH:
            raise ValueError(
                f"Nome deve possuir pelo menos {self.MIN_LENGTH} caracteres."
            )

        if len(name) > self.MAX_LENGTH:
            raise ValueError(
                f"Nome deve possuir no máximo {self.MAX_LENGTH} caracteres."
            )

        object.__setattr__(self, "value", name)

    def __str__(self) -> str:
        return self.value

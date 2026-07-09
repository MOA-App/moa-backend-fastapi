from dataclasses import dataclass


@dataclass(frozen=True)
class Password:
    """
    Value Object que representa uma senha criptografada.
    """

    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Senha não pode ser vazia.")

    def __str__(self) -> str:
        return self.value

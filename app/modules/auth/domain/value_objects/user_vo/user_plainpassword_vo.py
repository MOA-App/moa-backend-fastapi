from dataclasses import dataclass
import re


@dataclass(frozen=True)
class PlainPassword:
    """
    Value Object que representa uma senha em texto puro.

    É utilizado apenas durante operações como:
    - Cadastro
    - Login
    - Alteração de senha

    Nunca deve ser persistido.
    """

    value: str

    MIN_LENGTH = 8
    MAX_LENGTH = 128

    def __post_init__(self):
        password = self.value.strip()

        if not password:
            raise ValueError("A senha não pode ser vazia.")

        if len(password) < self.MIN_LENGTH:
            raise ValueError(
                f"A senha deve possuir pelo menos {self.MIN_LENGTH} caracteres."
            )

        if len(password) > self.MAX_LENGTH:
            raise ValueError(
                f"A senha deve possuir no máximo {self.MAX_LENGTH} caracteres."
            )

        if not re.search(r"[A-Z]", password):
            raise ValueError(
                "A senha deve conter pelo menos uma letra maiúscula."
            )

        if not re.search(r"[a-z]", password):
            raise ValueError(
                "A senha deve conter pelo menos uma letra minúscula."
            )

        if not re.search(r"\d", password):
            raise ValueError(
                "A senha deve conter pelo menos um número."
            )

        if not re.search(r"[!@#$%^&*()_\-+=\[\]{}|\\:;\"'<>,.?/~`]", password):
            raise ValueError(
                "A senha deve conter pelo menos um caractere especial."
            )

        object.__setattr__(self, "value", password)

    def __str__(self) -> str:
        return self.value

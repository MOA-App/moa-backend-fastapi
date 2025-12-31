from dataclasses import dataclass

@dataclass(frozen=True)
class PersonName:
    """Value Object para Nome de Pessoa"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome não pode ser vazio")

        cleaned = self.value.strip()

        if len(cleaned) < 2:
            raise ValueError("Nome deve ter no mínimo 2 caracteres")

        if len(cleaned) > 255:
            raise ValueError("Nome deve ter no máximo 255 caracteres")

        if not self._is_valid_name(cleaned):
            raise ValueError(
                "Nome deve conter apenas letras e espaços"
            )

        normalized = " ".join(
            word.capitalize() for word in cleaned.split()
        )

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_name(name: str) -> bool:
        # Aceita letras (com acento) e espaços
        return all(
            part.isalpha()
            for part in name.replace(" ", "")
        )

    def __str__(self) -> str:
        return self.value

    def get_first_name(self) -> str:
        return self.value.split()[0]

    def get_last_name(self) -> str:
        parts = self.value.split()
        return parts[-1] if len(parts) > 1 else ""

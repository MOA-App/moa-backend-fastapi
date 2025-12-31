from dataclasses import dataclass
import re

@dataclass(frozen=True)
class PermissionName:
    """Value Object para Nome de Permissão (resource.action)"""
    value: str

    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome da permissão não pode ser vazio")

        normalized = self.value.strip().lower()

        if not self._is_valid_permission_format(normalized):
            raise ValueError(
                "Permissão deve estar no formato 'resource.action' "
                "(ex: users.create, users.posts.delete)"
            )

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_permission_format(name: str) -> bool:
        # letras, números e underscore, separados por pontos
        return re.match(r"^[a-z0-9_]+(\.[a-z0-9_]+)+$", name) is not None

    def get_resource(self) -> str:
        parts = self.value.split(".")
        return ".".join(parts[:-1])

    def get_action(self) -> str:
        return self.value.split(".")[-1]

    def __str__(self) -> str:
        return self.value


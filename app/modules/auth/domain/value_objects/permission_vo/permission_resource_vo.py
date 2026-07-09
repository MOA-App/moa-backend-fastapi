import re

class PermissionResource:
    __slots__ = ("_value",)

    def __init__(self, value: str):
        if not value:
            raise ValueError("Resource não pode ser vazio")

        if not re.match(r"^[a-z][a-z0-9_]*$", value):
            raise ValueError(
                "Resource deve conter apenas letras minúsculas, números ou _"
            )

        self._value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value

    def __eq__(self, other):
        return isinstance(other, PermissionResource) and self._value == other._value

    def __hash__(self):
        return hash(self._value)

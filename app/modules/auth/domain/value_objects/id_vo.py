from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass(frozen=True, eq=False)
class EntityId:
    """Value Object para ID de Entidade"""
    value: UUID

    @staticmethod
    def generate() -> "EntityId":
        return EntityId(uuid4())

    @staticmethod
    def from_string(id_str: str) -> "EntityId":
        try:
            return EntityId(UUID(id_str))
        except ValueError:
            raise ValueError(f"ID inválido: {id_str}")

    def __str__(self) -> str:
        return str(self.value)

    def __eq__(self, other: object) -> bool:
        return isinstance(other, EntityId) and self.value == other.value

    def __hash__(self) -> int:
        return hash(self.value)

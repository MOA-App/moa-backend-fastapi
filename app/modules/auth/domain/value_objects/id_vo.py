from uuid import UUID, uuid4
from dataclasses import dataclass


@dataclass(frozen=True)
class EntityId:
    """Value Object para ID de Entidade"""
    value: UUID
    
    @staticmethod
    def generate() -> 'EntityId':
        """Gera um novo ID"""
        return EntityId(uuid4())
    
    @staticmethod
    def from_string(id_str: str) -> 'EntityId':
        """Cria ID a partir de string"""
        try:
            return EntityId(UUID(id_str))
        except ValueError:
            raise ValueError(f"ID inválido: {id_str}")
    
    def __str__(self) -> str:
        return str(self.value)
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, EntityId):
            return False
        return self.value == other.value

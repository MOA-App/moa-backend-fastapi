from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Email:
    """Value Object para Email"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Email não pode ser vazio")
        
        if not self._is_valid_email(self.value):
            raise ValueError(f"Email inválido: {self.value}")
        
        # Normaliza o email para lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
    
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def __str__(self) -> str:
        return self.value
    
    def __eq__(self, other) -> bool:
        if not isinstance(other, Email):
            return False
        return self.value == other.value

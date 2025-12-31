from dataclasses import dataclass
import re

@dataclass(frozen=True)
class RoleName:
    """Value Object para Nome de Role"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome da role não pode ser vazio")
        
        if len(self.value) < 2:
            raise ValueError("Nome da role deve ter no mínimo 2 caracteres")
        
        if len(self.value) > 100:
            raise ValueError("Nome da role deve ter no máximo 100 caracteres")
        
        if not self._is_valid_role_name(self.value):
            raise ValueError(
                "Nome da role deve conter apenas letras, números e underscores"
            )
        
        # Normaliza para lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
    
    @staticmethod
    def _is_valid_role_name(name: str) -> bool:
        pattern = r'^[a-zA-Z0-9_]+$'
        return re.match(pattern, name) is not None
    
    def __str__(self) -> str:
        return self.value

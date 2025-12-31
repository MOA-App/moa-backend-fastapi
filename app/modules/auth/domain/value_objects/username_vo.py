from dataclasses import dataclass
import re

@dataclass(frozen=True)
class Username:
    """Value Object para Nome de Usuário"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome de usuário não pode ser vazio")
        
        if len(self.value) < 3:
            raise ValueError("Nome de usuário deve ter no mínimo 3 caracteres")
        
        if len(self.value) > 50:
            raise ValueError("Nome de usuário deve ter no máximo 50 caracteres")
        
        if not self._is_valid_username(self.value):
            raise ValueError(
                "Nome de usuário deve conter apenas letras, números, "
                "underscores e hífens"
            )
        
        # Normaliza para lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
    
    @staticmethod
    def _is_valid_username(username: str) -> bool:
        pattern = r'^[a-zA-Z0-9_-]+$'
        return re.match(pattern, username) is not None
    
    def __str__(self) -> str:
        return self.value

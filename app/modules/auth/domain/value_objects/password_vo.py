from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Password:
    """Value Object para Password (senha não hasheada)"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Senha não pode ser vazia")
        
        if len(self.value) < 8:
            raise ValueError("Senha deve ter no mínimo 8 caracteres")
        
        if len(self.value) > 128:
            raise ValueError("Senha deve ter no máximo 128 caracteres")
        
        if not self._has_minimum_strength(self.value):
            raise ValueError(
                "Senha deve conter pelo menos: "
                "1 letra maiúscula, 1 letra minúscula, 1 número"
            )
    
    @staticmethod
    def _has_minimum_strength(password: str) -> bool:
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        return has_upper and has_lower and has_digit
    
    def __str__(self) -> str:
        return "********"  # Nunca expõe a senha
    
    def __repr__(self) -> str:
        return "Password(********)"

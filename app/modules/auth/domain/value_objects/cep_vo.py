from dataclasses import dataclass
import re

@dataclass(frozen=True)
class CEP:
    """Value Object para CEP (código postal brasileiro)"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("CEP não pode ser vazio")
        
        # Remove caracteres não numéricos
        cleaned = re.sub(r'\D', '', self.value)
        
        if len(cleaned) != 8:
            raise ValueError("CEP deve ter 8 dígitos")
        
        # Formata como XXXXX-XXX
        formatted = f"{cleaned[:5]}-{cleaned[5:]}"
        object.__setattr__(self, 'value', formatted)
    
    def __str__(self) -> str:
        return self.value
    
    def get_unformatted(self) -> str:
        """Retorna CEP sem formatação"""
        return self.value.replace('-', '')

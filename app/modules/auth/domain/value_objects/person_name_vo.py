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
        
        # Normaliza o nome: capitaliza cada palavra
        normalized = ' '.join(word.capitalize() for word in cleaned.split())
        object.__setattr__(self, 'value', normalized)
    
    def __str__(self) -> str:
        return self.value
    
    def get_first_name(self) -> str:
        """Retorna o primeiro nome"""
        return self.value.split()[0]
    
    def get_last_name(self) -> str:
        """Retorna o último nome"""
        parts = self.value.split()
        return parts[-1] if len(parts) > 1 else ""

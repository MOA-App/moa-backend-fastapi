from dataclasses import dataclass

@dataclass(frozen=True)
class HashedPassword:
    """Value Object para senha já hasheada"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Hash da senha não pode ser vazio")
        
        # Bcrypt hash sempre começa com $2a$, $2b$ ou $2y$
        if not (self.value.startswith('$2a$') or 
                self.value.startswith('$2b$') or 
                self.value.startswith('$2y$')):
            raise ValueError("Hash de senha inválido")
    
    def __str__(self) -> str:
        return self.value

from dataclasses import dataclass

from app.modules.auth.domain.value_objects.cep_vo import CEP

@dataclass(frozen=True)
class Address:
    """Value Object para Endereço Completo"""
    rua: str
    cidade: str
    estado: str
    cep: CEP
    pais: str
    
    def __post_init__(self):
        # Valida rua
        if not self.rua or len(self.rua.strip()) < 3:
            raise ValueError("Rua deve ter no mínimo 3 caracteres")
        
        # Valida cidade
        if not self.cidade or len(self.cidade.strip()) < 2:
            raise ValueError("Cidade deve ter no mínimo 2 caracteres")
        
        # Valida estado (sigla brasileira)
        ESTADOS_BR = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        estado_upper = self.estado.upper().strip()
        if estado_upper not in ESTADOS_BR:
            raise ValueError(f"Estado inválido: {self.estado}")
        
        object.__setattr__(self, 'estado', estado_upper)
        
        # Valida país
        if not self.pais or len(self.pais.strip()) < 2:
            raise ValueError("País deve ter no mínimo 2 caracteres")
        
        # Normaliza strings
        object.__setattr__(self, 'rua', self.rua.strip())
        object.__setattr__(self, 'cidade', self.cidade.strip().title())
        object.__setattr__(self, 'pais', self.pais.strip().title())
    
    def get_formatted(self) -> str:
        """Retorna endereço formatado"""
        return f"{self.rua}, {self.cidade} - {self.estado}, {self.cep}, {self.pais}"
    
    def __str__(self) -> str:
        return self.get_formatted()

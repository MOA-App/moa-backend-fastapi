from dataclasses import dataclass
import re

@dataclass(frozen=True)
class PermissionName:
    """Value Object para Nome de Permissão (formato: resource.action)"""
    value: str
    
    def __post_init__(self):
        if not self.value:
            raise ValueError("Nome da permissão não pode ser vazio")
        
        if not self._is_valid_permission_format(self.value):
            raise ValueError(
                "Permissão deve estar no formato 'resource.action' "
                "(ex: users.create, posts.delete)"
            )
        
        # Normaliza para lowercase
        object.__setattr__(self, 'value', self.value.lower().strip())
    
    @staticmethod
    def _is_valid_permission_format(name: str) -> bool:
        # Formato: resource.action (pode ter múltiplos níveis: users.posts.create)
        pattern = r'^[a-z_]+(\.[a-z_]+)+$'
        return re.match(pattern, name.lower()) is not None
    
    def get_resource(self) -> str:
        """Retorna o recurso da permissão (parte antes do último ponto)"""
        parts = self.value.split('.')
        return '.'.join(parts[:-1])
    
    def get_action(self) -> str:
        """Retorna a ação da permissão (parte depois do último ponto)"""
        return self.value.split('.')[-1]
    
    def __str__(self) -> str:
        return self.value

from dataclasses import dataclass
import re
from typing import List

from app.modules.auth.domain.exceptions.auth_exceptions import InvalidPermissionFormatException
from app.modules.auth.domain.value_objects.permission_resource_vo import PermissionResource


@dataclass(frozen=True, eq=True)  # ← Adicionar eq=True
class PermissionName:
    """
    Value Object para Nome de Permissão.
    
    Formato: resource.action ou resource.subresource.action
    
    Examples:
        - users.create
        - users.read
        - admin.users.delete
        - posts.comments.moderate
    
    Rules:
        - Apenas lowercase
        - Partes separadas por ponto
        - Apenas letras, números e underscore em cada parte
        - Mínimo 2 partes (resource.action)
    """
    value: str

    def __post_init__(self):
        if not self.value:
            raise InvalidPermissionFormatException("Nome da permissão não pode ser vazio")

        normalized = self.value.strip().lower()

        # Validar comprimento
        if len(normalized) < 3:
            raise InvalidPermissionFormatException("Nome da permissão muito curto (mínimo 3 caracteres)")
        
        if len(normalized) > 100:
            raise InvalidPermissionFormatException("Nome da permissão muito longo (máximo 100 caracteres)")

        # Validar formato
        if not self._is_valid_permission_format(normalized):
            raise InvalidPermissionFormatException(
                "Permissão deve estar no formato 'resource.action' "
                "(ex: users.create, admin.users.delete). "
                "Use apenas letras, números e underscore, separados por pontos."
            )

        object.__setattr__(self, "value", normalized)

    @staticmethod
    def _is_valid_permission_format(name: str) -> bool:
        """
        Valida formato da permissão.
        
        Padrão: palavra.palavra ou palavra.palavra.palavra
        Palavra: [a-z0-9_]+
        """
        # Mínimo 2 partes, máximo 5 níveis de profundidade
        parts = name.split(".")
        if len(parts) < 2 or len(parts) > 5:
            return False
        
        # Cada parte deve conter apenas letras, números e underscore
        pattern = r"^[a-z0-9_]+$"
        return all(re.match(pattern, part) for part in parts)

    @property
    def resource(self) -> PermissionResource:
        """
        Retorna o recurso da permissão (tudo antes da última parte).
        
        Examples:
            users.create -> users
            admin.users.delete -> admin.users
        """
        parts = self.value.split(".")
        return PermissionResource(self.get_base_resource())

    @property
    def action(self) -> str:
        """
        Retorna a ação da permissão (última parte).
        
        Examples:
            users.create -> create
            admin.users.delete -> delete
        """
        return self.value.split(".")[-1]
    
    def get_parts(self) -> List[str]:
        """
        Retorna todas as partes da permissão.
        
        Returns:
            List[str]: Lista de partes
            
        Example:
            admin.users.delete -> ['admin', 'users', 'delete']
        """
        return self.value.split(".")
    
    def get_depth(self) -> int:
        """
        Retorna profundidade da permissão (quantidade de níveis).
        
        Examples:
            users.create -> 2
            admin.users.delete -> 3
        """
        return len(self.get_parts())
    
    def is_nested(self) -> bool:
        """Verifica se a permissão tem mais de 2 níveis"""
        return self.get_depth() > 2
    
    def get_base_resource(self) -> str:
        """
        Retorna recurso base (primeira parte).
        
        Examples:
            users.create -> users
            admin.users.delete -> admin
        """
        return self.get_parts()[0]

    def __str__(self) -> str:
        return self.value
    
    def __repr__(self) -> str:
        return f"PermissionName('{self.value}')"

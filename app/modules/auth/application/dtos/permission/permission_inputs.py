from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import re


# ============================================================================
# INPUT DTOs (Request)
# ============================================================================

class CreatePermissionDTO(BaseModel):
    """
    DTO para criar nova permissão.
    
    Validações:
    - Nome no formato resource.action
    - Apenas lowercase, números e underscore
    - Descrição opcional
    """
    nome: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Nome da permissão no formato resource.action",
        examples=["users.create", "posts.delete", "admin.users.manage"]
    )
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Descrição da permissão",
        examples=["Permite criar novos usuários no sistema"]
    )
    
    @field_validator('nome')
    @classmethod
    def validate_permission_format(cls, v: str) -> str:
        """Valida formato da permissão"""
        normalized = v.strip().lower()
        
        # Formato: palavra.palavra (mínimo 2 partes, máximo 5)
        parts = normalized.split(".")
        if len(parts) < 2:
            raise ValueError(
                'Permissão deve ter pelo menos 2 partes: "resource.action"'
            )
        
        if len(parts) > 5:
            raise ValueError(
                'Permissão não pode ter mais de 5 níveis de profundidade'
            )
        
        # Cada parte deve conter apenas letras, números e underscore
        pattern = r'^[a-z0-9_]+$'
        for i, part in enumerate(parts):
            if not re.match(pattern, part):
                raise ValueError(
                    f'Parte "{part}" inválida. Use apenas letras minúsculas, '
                    f'números e underscore'
                )
        
        return normalized
    
    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v: Optional[str]) -> Optional[str]:
        """Valida e limpa descrição"""
        if v is None:
            return None
        
        cleaned = v.strip()
        if not cleaned:
            return None
        
        return cleaned
    
    class Config:
        json_schema_extra = {
            "example": {
                "nome": "users.create",
                "descricao": "Permite criar novos usuários no sistema"
            }
        }


class UpdatePermissionDTO(BaseModel):
    """
    DTO para atualizar permissão existente.
    
    Permite atualizar apenas a descrição.
    O nome não pode ser alterado (criar nova permissão).
    """
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Nova descrição da permissão"
    )
    
    @field_validator('descricao')
    @classmethod
    def validate_descricao(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        cleaned = v.strip()
        return cleaned if cleaned else None
    
    class Config:
        json_schema_extra = {
            "example": {
                "descricao": "Descrição atualizada da permissão"
            }
        }


class AssignPermissionToRoleDTO(BaseModel):
    """DTO para atribuir permissão a uma role"""
    role_id: UUID = Field(..., description="ID da role")
    permission_id: UUID = Field(..., description="ID da permissão")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_id": "123e4567-e89b-12d3-a456-426614174000",
                "permission_id": "987fcdeb-51a2-43f7-9876-543210fedcba"
            }
        }


class RevokePermissionFromRoleDTO(BaseModel):
    """DTO para remover permissão de uma role"""
    role_id: UUID = Field(..., description="ID da role")
    permission_id: UUID = Field(..., description="ID da permissão")
    
    class Config:
        json_schema_extra = {
            "example": {
                "role_id": "123e4567-e89b-12d3-a456-426614174000",
                "permission_id": "987fcdeb-51a2-43f7-9876-543210fedcba"
            }
        }

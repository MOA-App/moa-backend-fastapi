from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from uuid import UUID
from datetime import datetime
import re


class PermissionResponseDTO(BaseModel):
    """DTO de resposta para Permission"""
    id: UUID
    nome: str
    descricao: Optional[str] = None
    data_criacao: datetime
    
    # Metadados derivados
    resource: str = Field(description="Recurso da permissão (ex: users)")
    action: str = Field(description="Ação da permissão (ex: create)")
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "987fcdeb-51a2-43f7-9876-543210fedcba",
                "nome": "users.create",
                "descricao": "Permite criar novos usuários",
                "data_criacao": "2024-01-15T10:30:00",
                "resource": "users",
                "action": "create"
            }
        }


class PermissionSummaryDTO(BaseModel):
    """DTO resumido de Permission (para listagens)"""
    id: UUID
    nome: str
    descricao: Optional[str] = None
    
    class Config:
        from_attributes = True


class PermissionDetailDTO(BaseModel):
    """DTO detalhado de Permission com relacionamentos"""
    id: UUID
    nome: str
    descricao: Optional[str] = None
    data_criacao: datetime
    resource: str
    action: str
    
    # Relacionamentos
    roles_count: int = Field(
        default=0,
        description="Quantidade de roles que possuem esta permissão"
    )
    users_count: int = Field(
        default=0,
        description="Quantidade de usuários que possuem esta permissão (via roles)"
    )
    
    class Config:
        from_attributes = True


class PermissionsByResourceDTO(BaseModel):
    """DTO para agrupar permissões por recurso"""
    resource: str
    permissions: List[PermissionSummaryDTO]
    total: int = Field(description="Total de permissões deste recurso")
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource": "users",
                "permissions": [
                    {"id": "uuid1", "nome": "users.create", "descricao": "Criar"},
                    {"id": "uuid2", "nome": "users.read", "descricao": "Ler"}
                ],
                "total": 2
            }
        }


class ResourceActionsDTO(BaseModel):
    """DTO para listar ações disponíveis de um recurso"""
    resource: str
    actions: List[str] = Field(
        description="Lista de ações disponíveis",
        examples=[["create", "read", "update", "delete"]]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "resource": "users",
                "actions": ["create", "read", "update", "delete", "manage"]
            }
        }


class PermissionStatsDTO(BaseModel):
    """DTO para estatísticas de permissões"""
    total_permissions: int
    total_resources: int
    resources: List[str]
    most_used_permissions: List[PermissionSummaryDTO] = Field(
        max_length=10,
        description="Top 10 permissões mais usadas"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_permissions": 45,
                "total_resources": 8,
                "resources": ["users", "posts", "comments", "admin"],
                "most_used_permissions": []
            }
        }

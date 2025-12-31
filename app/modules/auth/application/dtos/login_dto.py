class LoginDTO(BaseModel):
    """DTO para login de usuário"""
    email: EmailStr = Field(..., examples=["joao.silva@example.com"])
    senha: str = Field(..., min_length=1, examples=["MinhaSenh@123"])


# app/modules/auth/application/dtos/user_response_dto.py
from uuid import UUID
from datetime import datetime
from typing import List


class PermissionResponseDTO(BaseModel):
    """DTO de resposta para Permission"""
    id: UUID
    nome: str
    descricao: Optional[str] = None
    data_criacao: datetime
    
    class Config:
        from_attributes = True


class RoleResponseDTO(BaseModel):
    """DTO de resposta para Role"""
    id: UUID
    nome: str
    permissions: List[PermissionResponseDTO] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class EnderecoResponseDTO(BaseModel):
    """DTO de resposta para Endereco"""
    id: UUID
    rua: str
    cidade: str
    estado: str
    cep: str
    pais: str
    
    class Config:
        from_attributes = True


class UserResponseDTO(BaseModel):
    """DTO de resposta para User"""
    id: UUID
    nome: str
    email: str
    nome_usuario: str
    data_cadastro: datetime
    roles: List[RoleResponseDTO] = Field(default_factory=list)
    enderecos: List[EnderecoResponseDTO] = Field(default_factory=list)
    
    class Config:
        from_attributes = True


class UserSummaryDTO(BaseModel):
    """DTO resumido de User (para listagens)"""
    id: UUID
    nome: str
    email: str
    nome_usuario: str
    
    class Config:
        from_attributes = True

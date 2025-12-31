from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
import re


class RegisterDTO(BaseModel):
    """DTO para registro de novo usuário"""
    nome: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nome completo do usuário",
        examples=["João da Silva"]
    )
    
    email: EmailStr = Field(
        ...,
        description="Email válido do usuário",
        examples=["joao.silva@example.com"]
    )
    
    senha: str = Field(
        ...,
        min_length=8,
        max_length=128,
        description="Senha com no mínimo 8 caracteres",
        examples=["MinhaSenh@123"]
    )
    
    nome_usuario: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Nome de usuário único",
        examples=["joao_silva"]
    )
    
    id_token_firebase: Optional[str] = Field(
        None,
        max_length=500
    )
    
    @field_validator('senha')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v
    
    @field_validator('nome_usuario')
    @classmethod
    def validate_username_format(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_-]+$', v):
            raise ValueError('Nome de usuário deve conter apenas letras, números, _ e -')
        return v

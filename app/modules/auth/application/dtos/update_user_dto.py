class UpdateEmailDTO(BaseModel):
    """DTO para atualizar email"""
    email: EmailStr


class UpdateUsernameDTO(BaseModel):
    """DTO para atualizar username"""
    username: str = Field(..., min_length=3, max_length=50, pattern=r'^[a-zA-Z0-9_-]+$')


class UpdatePasswordDTO(BaseModel):
    """DTO para atualizar senha"""
    senha_atual: str = Field(..., min_length=1)
    senha_nova: str = Field(..., min_length=8, max_length=128)
    
    @field_validator('senha_nova')
    @classmethod
    def validate_password_strength(cls, v: str) -> str:
        if not re.search(r'[A-Z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra maiúscula')
        if not re.search(r'[a-z]', v):
            raise ValueError('Senha deve conter pelo menos uma letra minúscula')
        if not re.search(r'\d', v):
            raise ValueError('Senha deve conter pelo menos um número')
        return v


class UpdateUserDTO(BaseModel):
    """DTO para atualizar dados do usuário"""
    nome: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    nome_usuario: Optional[str] = Field(None, min_length=3, max_length=50)

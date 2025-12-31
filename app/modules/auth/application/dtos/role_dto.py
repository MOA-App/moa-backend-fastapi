class CreateRoleDTO(BaseModel):
    """DTO para criar role"""
    nome: str = Field(..., min_length=2, max_length=100)
    
    @field_validator('nome')
    @classmethod
    def validate_role_name(cls, v: str) -> str:
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('Nome da role deve conter apenas letras, números e _')
        return v


class AssignRoleDTO(BaseModel):
    """DTO para atribuir role a usuário"""
    user_id: UUID
    role_id: UUID

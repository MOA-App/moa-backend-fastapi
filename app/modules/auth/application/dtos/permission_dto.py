class CreatePermissionDTO(BaseModel):
    """DTO para criar permissão"""
    nome: str = Field(..., min_length=2, max_length=100)
    descricao: Optional[str] = Field(None, max_length=500)
    
    @field_validator('nome')
    @classmethod
    def validate_permission_format(cls, v: str) -> str:
        if not re.match(r'^[a-z_]+\.[a-z_]+$', v.lower()):
            raise ValueError('Permissão deve estar no formato "resource.action"')
        return v


class AssignPermissionToRoleDTO(BaseModel):
    """DTO para atribuir permissão a role"""
    role_id: UUID
    permission_id: UUID

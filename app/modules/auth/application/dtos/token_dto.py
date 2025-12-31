class TokenDTO(BaseModel):
    """DTO de resposta para autenticação com token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
    user: UserResponseDTO

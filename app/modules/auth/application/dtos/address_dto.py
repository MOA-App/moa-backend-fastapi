class CreateAddressDTO(BaseModel):
    """DTO para criar endereço"""
    rua: str = Field(..., min_length=3, max_length=255)
    cidade: str = Field(..., min_length=2, max_length=100)
    estado: str = Field(..., min_length=2, max_length=2)
    cep: str = Field(..., pattern=r'^\d{5}-?\d{3}$')
    pais: str = Field(default="Brasil", max_length=100)


class UpdateAddressDTO(BaseModel):
    """DTO para atualizar endereço"""
    rua: Optional[str] = Field(None, min_length=3, max_length=255)
    cidade: Optional[str] = Field(None, min_length=2, max_length=100)
    estado: Optional[str] = Field(None, min_length=2, max_length=2)
    cep: Optional[str] = Field(None, pattern=r'^\d{5}-?\d{3}$')
    pais: Optional[str] = Field(None, max_length=100)

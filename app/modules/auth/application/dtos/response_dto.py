class ErrorResponseDTO(BaseModel):
    """DTO padrão para respostas de erro"""
    error: str
    message: str
    details: Optional[dict] = None


class SuccessResponseDTO(BaseModel):
    """DTO padrão para respostas de sucesso"""
    success: bool = True
    message: str
    data: Optional[dict] = None


class MessageResponseDTO(BaseModel):
    """DTO simples de resposta com mensagem"""
    message: str

class PaginationDTO(BaseModel):
    """DTO para paginação"""
    page: int = Field(default=1, ge=1, description="Número da página")
    page_size: int = Field(default=10, ge=1, le=100, description="Tamanho da página")
    
    @property
    def skip(self) -> int:
        return (self.page - 1) * self.page_size
    
    @property
    def limit(self) -> int:
        return self.page_size


class PaginatedResponseDTO(BaseModel):
    """DTO de resposta paginada"""
    items: List[dict]
    total: int
    page: int
    page_size: int
    total_pages: int
    
    @classmethod
    def create(cls, items: List, total: int, pagination: PaginationDTO):
        total_pages = (total + pagination.page_size - 1) // pagination.page_size
        return cls(
            items=items,
            total=total,
            page=pagination.page,
            page_size=pagination.page_size,
            total_pages=total_pages
        )

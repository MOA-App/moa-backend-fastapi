"""
Schemas da camada Presentation para o módulo Product.

Esses schemas são usados apenas nas routes (request/response da API).
Não confundir com os DTOs da Application Layer (CreateProductDTO,
UpdateProductDTO, ProductResponseDTO), que carregam as regras de
validação de entrada/saída dos use cases.

Aqui ficam:
- Schemas de erro padronizados (para documentação OpenAPI)
- Wrappers de resposta (listagem, paginação, stats)
- Schemas de query params, quando complexos
"""

from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================================================
# ERROR SCHEMAS
# ============================================================================

class ErrorResponseSchema(BaseModel):
    """Schema padrão de erro retornado pela API"""
    detail: str = Field(..., description="Mensagem descritiva do erro")

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Produto não encontrado"
            }
        }
    }


class ProductNotFoundErrorSchema(ErrorResponseSchema):
    """Schema de erro 404 - produto não encontrado"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Produto com ID 'xxxx-xxxx' não encontrado"
            }
        }
    }


class ProductConflictErrorSchema(ErrorResponseSchema):
    """Schema de erro 409 - produto já existe (SKU duplicado)"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Produto com SKU 'ABC-123' já existe"
            }
        }
    }


class CategoryNotFoundErrorSchema(ErrorResponseSchema):
    """Schema de erro 404 - categoria referenciada não encontrada"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Categoria com ID 'xxxx-xxxx' não encontrada"
            }
        }
    }


class ValidationErrorSchema(BaseModel):
    """Schema de erro de validação (422)"""
    detail: List[dict] = Field(
        ...,
        description="Lista de erros de validação por campo"
    )

    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": [
                    {
                        "loc": ["body", "price"],
                        "msg": "ensure this value is greater than 0",
                        "type": "value_error.number.not_gt"
                    }
                ]
            }
        }
    }


# ============================================================================
# QUERY PARAMS SCHEMAS
# ============================================================================

class ProductListQuerySchema(BaseModel):
    """Schema para query params da listagem de produtos"""
    skip: int = Field(0, ge=0, description="Número de registros a pular")
    limit: int = Field(100, ge=1, le=1000, description="Limite de registros")
    category_id: Optional[str] = Field(None, description="Filtrar por categoria")
    active_only: bool = Field(False, description="Apenas produtos ativos")


class ProductSearchQuerySchema(BaseModel):
    """Schema para query params da busca de produtos por nome"""
    name: str = Field(..., min_length=1, description="Nome ou parte do nome do produto")


class ProductSkuQuerySchema(BaseModel):
    """Schema para query params da busca por SKU"""
    sku: str = Field(..., min_length=1, description="Código SKU do produto")


# ============================================================================
# LIST / PAGINATION SCHEMAS
# ============================================================================

class ProductListResponseSchema(BaseModel):
    """Schema de resposta para listagem de produtos com metadados"""
    total: int = Field(..., description="Total de produtos encontrados")
    skip: int = Field(..., description="Registros pulados")
    limit: int = Field(..., description="Limite aplicado")
    items: List[dict] = Field(..., description="Lista de produtos (ProductResponseDTO)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 42,
                "skip": 0,
                "limit": 100,
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "Notebook Gamer",
                        "description": "Notebook para jogos de alta performance",
                        "price": "4999.90",
                        "sku": "NB-GAMER-001",
                        "category_id": "8f14e45f-ceea-4c7d-8a6e-1f2b3c4d5e6f",
                        "stock_quantity": 15,
                        "is_active": True,
                        "created_at": "2026-01-01T10:00:00",
                        "updated_at": "2026-01-01T10:00:00"
                    }
                ]
            }
        }
    }


# ============================================================================
# STATS SCHEMAS
# ============================================================================

class ProductStatsByCategorySchema(BaseModel):
    """Schema de resposta para contagem de produtos filtrada por categoria"""
    category_id: str = Field(..., description="ID da categoria filtrada")
    count: int = Field(..., description="Quantidade de produtos na categoria")

    model_config = {
        "json_schema_extra": {
            "example": {
                "category_id": "8f14e45f-ceea-4c7d-8a6e-1f2b3c4d5e6f",
                "count": 12
            }
        }
    }


class ProductStatsTotalSchema(BaseModel):
    """Schema de resposta para contagem total de produtos"""
    total: int = Field(..., description="Quantidade total de produtos cadastrados")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 128
            }
        }
    }


# ============================================================================
# PATH PARAM SCHEMA (opcional, útil para validar UUID nas rotas)
# ============================================================================

class ProductIdPathSchema(BaseModel):
    """Schema para validação do path param product_id"""
    product_id: str = Field(..., description="UUID do produto")

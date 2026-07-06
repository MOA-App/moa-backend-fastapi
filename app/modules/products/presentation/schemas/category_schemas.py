"""
Schemas da camada Presentation para o módulo Category.

Esses schemas são usados apenas nas routes (request/response da API).
Não confundir com os DTOs da Application Layer, que carregam regras
de validação de entrada/saída dos use cases.

Aqui ficam:
- Schemas de erro padronizados (para documentação OpenAPI)
- Wrappers de resposta (listagem, paginação, etc.)
- Schemas específicos de query params, quando complexos
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
                "detail": "Categoria não encontrada"
            }
        }
    }


class NotFoundErrorSchema(ErrorResponseSchema):
    """Schema de erro 404"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Categoria com ID 'xxxx-xxxx' não encontrada"
            }
        }
    }


class ConflictErrorSchema(ErrorResponseSchema):
    """Schema de erro 409 (conflito, ex: categoria já existe)"""
    model_config = {
        "json_schema_extra": {
            "example": {
                "detail": "Categoria com nome 'Eletrônicos' já existe"
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
                        "loc": ["body", "name"],
                        "msg": "field required",
                        "type": "value_error.missing"
                    }
                ]
            }
        }
    }


# ============================================================================
# LIST / PAGINATION SCHEMAS
# ============================================================================

class CategoryListQuerySchema(BaseModel):
    """Schema para query params da listagem de categorias"""
    skip: int = Field(0, ge=0, description="Quantidade de registros para pular")
    limit: int = Field(50, ge=1, le=200, description="Quantidade máxima de registros")
    search: Optional[str] = Field(
        None, min_length=1, max_length=120,
        description="Filtra categorias pelo nome (busca parcial)"
    )


class CategoryListResponseSchema(BaseModel):
    """Schema de resposta para listagem de categorias com metadados"""
    total: int = Field(..., description="Total de categorias encontradas")
    skip: int = Field(..., description="Registros pulados")
    limit: int = Field(..., description="Limite aplicado")
    items: List[dict] = Field(..., description="Lista de categorias (CategoryResponseDTO)")

    model_config = {
        "json_schema_extra": {
            "example": {
                "total": 12,
                "skip": 0,
                "limit": 50,
                "items": [
                    {
                        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                        "name": "Eletrônicos",
                        "description": "Produtos eletrônicos em geral",
                        "created_at": "2026-01-01T10:00:00",
                        "updated_at": "2026-01-01T10:00:00"
                    }
                ]
            }
        }
    }


# ============================================================================
# PATH PARAM SCHEMA (opcional, útil se quiser validar UUID nas rotas)
# ============================================================================

class CategoryIdPathSchema(BaseModel):
    """Schema para validação do path param category_id"""
    category_id: str = Field(..., description="UUID da categoria")

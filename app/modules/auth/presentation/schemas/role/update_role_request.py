from pydantic import BaseModel, Field, field_validator
import re


class UpdateRoleRequest(BaseModel):
    """Schema de entrada para atualização de uma role."""

    nome: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Novo nome da role. Apenas letras minúsculas, números e underscores.",
        examples=["super_admin"],
    )

    @field_validator("nome")
    @classmethod
    def validate_nome(cls, v: str) -> str:
        normalized = v.strip().lower()
        if not re.match(r"^[a-z0-9_]+$", normalized):
            raise ValueError(
                "Nome da role deve conter apenas letras minúsculas, números e underscores"
            )
        return normalized

    model_config = {"str_strip_whitespace": True}

    class Config:
        json_schema_extra = {
            "example": {
                "nome": "super_admin",
            }
        }

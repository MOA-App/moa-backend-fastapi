from typing import List
from pydantic import BaseModel, Field


class ResourceActions(BaseModel):
    resource: str = Field(..., description="Nome do recurso")
    actions: List[str] = Field(..., description="Ações disponíveis para o recurso")

from typing import List
from pydantic import BaseModel, Field

from .create_permission_schema import CreatePermissionRequest


class BulkCreatePermissionsRequest(BaseModel):
    """
    Schema de request para criação de permissões em lote.
    """

    permissions: List[CreatePermissionRequest] = Field(
        ...,
        min_length=1,
        description="Lista de permissões a serem criadas"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "permissions": [
                    {
                        "nome": "users.create",
                        "descricao": "Criar usuários"
                    },
                    {
                        "nome": "users.read",
                        "descricao": "Ler usuários"
                    },
                    {
                        "nome": "users.update",
                        "descricao": "Atualizar usuários"
                    }
                ]
            }
        }

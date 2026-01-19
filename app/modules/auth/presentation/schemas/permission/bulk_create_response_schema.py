from typing import List
from pydantic import BaseModel, Field
from .permission_response import PermissionResponse


class BulkCreatePermissionsResponse(BaseModel):
    created: List[PermissionResponse] = Field(..., description="Permissões criadas")
    skipped: List[str] = Field(..., description="Permissões ignoradas (já existiam)")
    errors: List[str] = Field(..., description="Permissões com erro")

    total_created: int
    total_skipped: int
    total_errors: int

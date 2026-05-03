from pydantic import BaseModel, ConfigDict, Field
from uuid import UUID


class AddPermissionToRoleRequest(BaseModel):
    """Schema de entrada para associar uma permissão a uma role."""

    permission_id: UUID = Field(
        ...,
        description="ID da permissão a ser associada à role",
    )

    model_config = ConfigDict(
        json_schema_extra = {
            "example": {
                "permission_id": "550e8400-e29b-41d4-a716-446655440000",
            }
        }
    )

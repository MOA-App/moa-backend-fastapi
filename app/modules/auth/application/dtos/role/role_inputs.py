from dataclasses import dataclass
from typing import Optional
from uuid import UUID

@dataclass(frozen=True)
class CreateRoleDTO:
    """DTO de entrada para criação de uma role."""
    name: str


@dataclass(frozen=True)
class UpdateRoleDTO:
    """DTO de entrada para atualização de uma role."""
    role_id: UUID
    name: Optional[str] = None


@dataclass(frozen=True)
class AddPermissionToRoleDTO:
    """DTO de entrada para associar uma permissão a uma role."""
    role_id: UUID
    permission_id: UUID


@dataclass(frozen=True)
class RemovePermissionFromRoleDTO:
    """DTO de entrada para remover uma permissão de uma role."""
    role_id: UUID
    permission_id: UUID

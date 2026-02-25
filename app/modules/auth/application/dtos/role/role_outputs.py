from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class PermissionSummaryDTO:
    """Resumo de uma permissão vinculada à role."""
    id: UUID
    name: str
    description: Optional[str]


@dataclass(frozen=True)
class RoleResponseDTO:
    """DTO de saída com os dados completos de uma role."""
    id: UUID
    name: str
    description: Optional[str]
    permissions: List[PermissionSummaryDTO] = field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class RoleListResponseDTO:
    """DTO de saída para listagem de roles."""
    roles: List[RoleResponseDTO]
    total: int

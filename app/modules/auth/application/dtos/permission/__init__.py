from .permission_inputs import (
    CreatePermissionDTO,
    UpdatePermissionDTO,
    AssignPermissionToRoleDTO,
    RevokePermissionFromRoleDTO,
)

from .permission_outputs import (
    PermissionResponseDTO,
    PermissionSummaryDTO,
)

from .permission_queries import ListPermissionsQueryDTO
from .permission_bulk import (
    BulkCreatePermissionsDTO,
    BulkCreatePermissionsResponseDTO,
)
BulkCreatePermissionsDTO

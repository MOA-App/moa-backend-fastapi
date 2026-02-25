from app.modules.auth.application.dtos.role.role_outputs import PermissionSummaryDTO, RoleResponseDTO
from app.modules.auth.domain.entities.role_entity import Role


def to_role_response_dto(role: Role) -> RoleResponseDTO:
    """Converte uma entidade Role para RoleResponseDTO."""
    permissions = [
        PermissionSummaryDTO(
            id=perm.id.value,
            name=perm.name.value,
            description=perm.description,
        )
        for perm in role.permissions
    ]

    return RoleResponseDTO(
        id=role.id.value,
        name=role.name.value,
        description=role.description,
        permissions=permissions,
        created_at=getattr(role, "created_at", None),
        updated_at=getattr(role, "updated_at", None),
    )

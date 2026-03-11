from app.modules.auth.application.dtos.role.role_outputs import PermissionSummaryDTO, RoleResponseDTO
from app.modules.auth.application.mappers.permission_mapper import PermissionMapper
from app.modules.auth.domain.entities.role_entity import Role


def to_role_response_dto(role: Role) -> RoleResponseDTO:
    """Converte uma entidade Role para RoleResponseDTO."""

    permissions = [
        PermissionMapper.to_summary_dto(perm)
        for perm in role.permissions
    ]

    return RoleResponseDTO(
        id=role.id.value,
        name=role.nome.value,
        permissions=permissions,
        created_at=getattr(role, "created_at", None),
        updated_at=getattr(role, "updated_at", None),
    )

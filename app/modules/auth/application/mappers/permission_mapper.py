from app.modules.auth.domain.entities.permission_entity import Permission
from app.modules.auth.application.dtos.permission.permission_outputs import (
    PermissionDetailDTO,
    PermissionResponseDTO,
    PermissionSummaryDTO,
    PermissionsByResourceDTO,
    ResourceActionsDTO
)


class PermissionMapper:

    @staticmethod
    def to_response_dto(permission: Permission) -> PermissionResponseDTO:
        return PermissionResponseDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao,
            data_criacao=permission.data_criacao,
            resource=permission.nome.resource.value,
            action=permission.nome.action
        )

    @staticmethod
    def to_summary_dto(permission: Permission) -> PermissionSummaryDTO:
        return PermissionSummaryDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao
        )
    
    @staticmethod
    def to_detail_dto(
        permission: Permission,
        roles_count: int = 0,
        users_count: int = 0
    ) -> PermissionDetailDTO:
        return PermissionDetailDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao,
            data_criacao=permission.data_criacao,
            resource=permission.nome.resource.value,
            action=permission.nome.action,
            roles_count=roles_count,
            users_count=users_count
        )
    
    @staticmethod
    def group_by_resource(
        permissions: list[Permission]
    ) -> list[PermissionsByResourceDTO]:

        grouped: dict[str, list[PermissionResponseDTO]] = {}

        for permission in permissions:
            resource = permission.nome.resource.value

            grouped.setdefault(resource, []).append(
                PermissionMapper.to_response_dto(permission)
            )

        return [
            PermissionsByResourceDTO(
                resource=resource,
                permissions=perms,
                total=len(perms)
            )
            for resource, perms in grouped.items()
        ]
    
    @staticmethod
    def group_actions_by_resource(
        permissions: list[Permission]
    ) -> list[ResourceActionsDTO]:

        grouped: dict[str, set[str]] = {}

        for permission in permissions:
            resource = permission.nome.resource.value
            action = permission.nome.action

            grouped.setdefault(resource, set()).add(action)

        return [
            ResourceActionsDTO(
                resource=resource,
                actions=sorted(actions)
            )
            for resource, actions in grouped.items()
        ]

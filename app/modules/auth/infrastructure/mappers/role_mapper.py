from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.value_objects.role_name_vo import RoleName
from app.shared.domain.value_objects.id_vo import EntityId

from app.modules.auth.infrastructure.models.role_model import RoleModel
from app.modules.auth.infrastructure.mappers.permission_mapper import PermissionMapper


class RoleMapper:
    """
    Mapper de infraestrutura para Role.

    Responsável por converter entre:
        - RoleModel (SQLAlchemy) ↔ Role (Entidade de Domínio)
    """

    @staticmethod
    def to_entity(model: RoleModel) -> Role:
        """
        Converte um RoleModel (ORM) para a entidade de domínio Role.

        Args:
            model: Instância do RoleModel vinda do banco

        Returns:
            Role: Entidade de domínio reconstruída
        """
        permissions = [
            PermissionMapper.to_entity(perm_model)
            for perm_model in (model.permissions or [])
        ]

        return Role.reconstruct(
            id=EntityId(model.id),
            nome=RoleName(model.nome),
            permissions=permissions,
        )

    @staticmethod
    def to_model(entity: Role) -> RoleModel:
        """
        Converte uma entidade de domínio Role para RoleModel (ORM).

        Não mapeia permissions aqui — o relacionamento Many-to-Many
        é gerenciado explicitamente no repository via tabela de associação.

        Args:
            entity: Entidade de domínio Role

        Returns:
            RoleModel: Model pronto para persistência
        """
        return RoleModel(
            id=entity.id.value,
            nome=entity.nome.value,
        )

from dataclasses import dataclass, field
from typing import Iterable, List

from app.modules.auth.domain.value_objects.permission_name_vo import PermissionName
from app.shared.domain.value_objects.id_vo import EntityId
from app.modules.auth.domain.entities.permission_entity import Permission
from ..value_objects.role_name_vo import RoleName


@dataclass(eq=False)
class Role:
    """Entidade Role (Papel/Função) do Domínio"""
    
    id: EntityId
    nome: RoleName
    _permissions: List[Permission] = field(default_factory=list, repr=False)

    # ---------- Factories ----------
    @classmethod
    def create(cls, nome: RoleName) -> "Role":
        return cls(
            id=EntityId.generate(),
            nome=nome,
            _permissions=[]
        )

    @classmethod
    def reconstruct(
        cls,
        id: EntityId,
        nome: RoleName,
        permissions: Iterable[Permission],
    ) -> "Role":
        return cls(
            id=id,
            nome=nome,
            _permissions=list(permissions),
        )

    # ---------- Behavior ----------

    def update_name(self, new_name: RoleName) -> None:
        """Atualiza o nome da role."""
        self.nome = new_name

    def add_permission(self, permission: Permission) -> None:
        if self.has_permission(permission.nome):
            return
        self._permissions.append(permission)

    def remove_permission(self, permission: Permission) -> None:
        self._permissions = [
            p for p in self._permissions if p.id != permission.id
        ]

    def clear_permissions(self) -> None:
        self._permissions.clear()

    def has_permission(self, permission_name: PermissionName) -> bool:
        return any(
            p.nome == permission_name
            for p in self._permissions
        )

    def permissions_by_resource(self, resource: str) -> List[Permission]:
        resource = resource.lower()
        return [
            p for p in self._permissions
            if p.is_for_resource(resource)
        ]

    # ---------- Getters seguros ----------

    @property
    def permissions(self) -> tuple[Permission, ...]:
        return tuple(self._permissions)

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Role) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

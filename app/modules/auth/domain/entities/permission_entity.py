from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from app.shared.domain.value_objects.id_vo import EntityId
from ..value_objects.permission_name_vo import PermissionName


@dataclass(eq=False)
class Permission:
    """Entidade Permission do Domínio"""

    id: EntityId
    nome: PermissionName
    descricao: Optional[str]
    data_criacao: datetime

    @classmethod
    def create(cls, nome: str, descricao: Optional[str] = None) -> "Permission":
        return cls(
            id=EntityId.generate(),
            nome=PermissionName(nome),
            descricao=descricao,
            data_criacao=datetime.now(datetime.timezone.utc),
        )

    @classmethod
    def reconstruct(
        cls,
        id: EntityId,
        nome: PermissionName,
        descricao: Optional[str],
        data_criacao: datetime,
    ) -> "Permission":
        return cls(id, nome, descricao, data_criacao)

    # ---------- Behavior ----------

    def update_description(self, new_description: str) -> None:
        self.descricao = new_description

    def is_for_resource(self, resource: str) -> bool:
        return self.nome.get_resource() == resource.lower()

    def is_action(self, action: str) -> bool:
        return self.nome.get_action() == action.lower()

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Permission) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

    def __str__(self) -> str:
        return f"Permission({self.nome.value})"

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List

from app.modules.auth.domain.entities.endereco_entity import Endereco
from app.modules.auth.domain.entities.permission_entity import Permission
from app.modules.auth.domain.entities.role_entity import Role

from ..value_objects.email_vo import Email
from ..value_objects.password_vo import HashedPassword
from ..value_objects.username_vo import Username
from ..value_objects.person_name_vo import PersonName
from app.shared.domain.value_objects.id_vo import EntityId


@dataclass(eq=False)
class User:
    """Aggregate Root User"""

    id: EntityId
    nome: PersonName
    email: Email
    senha: HashedPassword
    nome_usuario: Username
    id_token_firebase: Optional[str]
    data_cadastro: datetime
    _roles: List[Role] = field(default_factory=list, repr=False)
    _enderecos: List[Endereco] = field(default_factory=list, repr=False)

    # ---------- Factories ----------

    @classmethod
    def create(
        cls,
        nome: str,
        email: str,
        senha_hash: str,
        nome_usuario: str,
        id_token_firebase: Optional[str] = None
    ) -> "User":
        return cls(
            id=EntityId.generate(),
            nome=PersonName(nome),
            email=Email(email),
            senha=HashedPassword(senha_hash),
            nome_usuario=Username(nome_usuario),
            id_token_firebase=id_token_firebase,
            data_cadastro=datetime.now(timezone.utc)
        )

    @classmethod
    def reconstruct(
        cls,
        id: EntityId,
        nome: PersonName,
        email: Email,
        senha: HashedPassword,
        nome_usuario: Username,
        id_token_firebase: Optional[str],
        data_cadastro: datetime,
        roles: List[Role],
        enderecos: List[Endereco],
    ) -> "User":
        return cls(
            id=id,
            nome=nome,
            email=email,
            senha=senha,
            nome_usuario=nome_usuario,
            id_token_firebase=id_token_firebase,
            data_cadastro=data_cadastro,
            _roles=list(roles),
            _enderecos=list(enderecos),
        )

    # ---------- Roles ----------

    def add_role(self, role: Role) -> None:
        if role.id in {r.id for r in self._roles}:
            return
        self._roles.append(role)

    def remove_role(self, role_id: EntityId) -> None:
        self._roles = [r for r in self._roles if r.id != role_id]

    def has_role(self, role_name: Role) -> bool:
        return any(r.nome.value == role_name.lower() for r in self._roles)

    def has_permission(self, permission_name: Permission) -> bool:
        return any(
            role.has_permission(permission_name)
            for role in self._roles
        )

    @property
    def roles(self) -> tuple[Role, ...]:
        return tuple(self._roles)

    # ---------- Endereços ----------

    def add_endereco(self, endereco: Endereco) -> None:
        if endereco.id in {e.id for e in self._enderecos}:
            return
        self._enderecos.append(endereco)

    def remove_endereco(self, endereco_id: EntityId) -> None:
        self._enderecos = [
            e for e in self._enderecos if e.id != endereco_id
        ]

    def get_endereco_principal(self) -> Optional[Endereco]:
        return self._enderecos[0] if self._enderecos else None

    @property
    def enderecos(self) -> tuple[Endereco, ...]:
        return tuple(self._enderecos)

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

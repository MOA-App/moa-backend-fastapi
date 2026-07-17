from dataclasses import dataclass, field, replace
from datetime import datetime, timezone
from typing import Optional, Iterable

from app.modules.auth.domain.exceptions.auth_exceptions import RoleAlreadyAssignedException, RoleNotAssignedException
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName
from app.modules.auth.domain.value_objects.user_vo.user_password_vo import Password
from app.shared.domain.value_objects.id_vo import EntityId

from .role_entity import Role


@dataclass(eq=False)
class User:
    """
    Entidade de domínio que representa um usuário do sistema.
    """

    id: EntityId
    name: UserName
    email: Email
    password: Password
    is_active: bool
    roles: list[Role] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # ---------- Factories ----------

    @classmethod
    def create(
        cls,
        name: UserName,
        email: Email,
        password: Password,
    ) -> "User":
        return cls(
            id=EntityId.generate(),
            name=name,
            email=email,
            password=password,
            is_active=True,
            roles=[],
            created_at=datetime.now(timezone.utc),
        )

    @classmethod
    def reconstruct(
        cls,
        id: EntityId,
        name: UserName,
        email: Email,
        password: Password,
        is_active: bool,
        created_at: datetime,
        roles: Iterable[Role],
    ) -> "User":
        return cls(
            id=id,
            name=name,
            email=email,
            password=password,
            is_active=is_active,
            created_at=created_at,
            roles=list(roles),
        )

    # ---------- Behavior ----------

    def activate(self) -> None:
        self.is_active = True

    def deactivate(self) -> None:
        self.is_active = False

    def change_name(self, name: UserName) -> None:
        self.name = name

    def change_email(self, email: Email) -> None:
        self.email = email

    def change_password(self, password: Password) -> None:
        self.password = password

    def add_role(self, role: Role) -> None:
        if role in self.roles:
            raise RoleAlreadyAssignedException()

        self.roles.append(role)

    def remove_role(self, role: Role) -> None:
        if role not in self.roles:
            raise RoleNotAssignedException()

        self.roles.remove(role)

    def has_role(self, role_name: str) -> bool:
        return any(
            role.nome.value == role_name.lower()
            for role in self.roles
        )

    def has_permission(self, permission_name: str) -> bool:
        return any(
            permission.get_full_name() == permission_name.lower()
            for role in self.roles
            for permission in role.permissions
        )

    def has_permission_pattern(self, pattern: str) -> bool:
        return any(
            permission.matches(pattern)
            for role in self.roles
            for permission in role.permissions
        )

    # ---------- Identity ----------

    def __eq__(self, other: object) -> bool:
        return isinstance(other, User) and self.id == other.id

    def __hash__(self) -> int:
        return hash(self.id)

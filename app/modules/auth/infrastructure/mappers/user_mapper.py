from typing import List

from app.modules.auth.domain.entities.user_entity import User
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_password_vo import Password

from app.modules.auth.infrastructure.models.user_model import UserModel
from app.modules.auth.infrastructure.mappers.role_mapper import RoleMapper

from app.shared.domain.value_objects.id_vo import EntityId


class UserMapper:
    """
    Mapper de infraestrutura para User.

    Responsável por converter entre:
        - UserModel (SQLAlchemy) ↔ User (Domínio)
    """

    @staticmethod
    def to_entity(model: UserModel) -> User:
        """
        Converte um UserModel em User.
        """

        roles = [
            RoleMapper.to_entity(role_model)
            for role_model in (model.roles or [])
        ]

        return User.reconstruct(
            id=EntityId(model.id),
            name=UserName(model.name),
            email=Email(model.email),
            password=Password(model.password),
            is_active=model.is_active,
            created_at=model.created_at,
            roles=roles,
        )

    @staticmethod
    def to_model(entity: User) -> UserModel:
        """
        Converte User para UserModel.

        Não mapeia roles. O relacionamento many-to-many é
        responsabilidade do repository.
        """

        return UserModel(
            id=entity.id.value,
            name=entity.name.value,
            email=entity.email.value,
            password=entity.password.value,
            is_active=entity.is_active,
            created_at=entity.created_at,
        )

    @staticmethod
    def update_model_from_entity(
        model: UserModel,
        entity: User,
    ) -> None:
        """
        Atualiza um UserModel existente.
        """

        model.name = entity.name.value
        model.email = entity.email.value
        model.password = entity.password.value
        model.is_active = entity.is_active

    @staticmethod
    def to_entities(models: List[UserModel]) -> List[User]:
        """
        Converte uma lista de UserModel em lista de User.
        """

        return [
            UserMapper.to_entity(model)
            for model in models
        ]

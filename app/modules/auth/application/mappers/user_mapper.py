from app.modules.auth.application.dtos.user.user_response_dto import UserResponse
from app.modules.auth.domain.entities.user_entity import User


class UserMapper:
    """
    Responsável por converter entre User (Domain)
    e UserDTO (Application).
    """

    @staticmethod
    def to_dto(user: User) -> UserResponse:
        return UserResponse(
            id=user.id.value,
            name=user.name.value,
            email=user.email.value,
            is_active=user.is_active,
            roles=[role.nome.value for role in user.roles],
            created_at=user.created_at,
        )

    @staticmethod
    def to_dto_list(users: list[User]) -> list[UserResponse]:
        return [UserMapper.to_dto(user) for user in users]

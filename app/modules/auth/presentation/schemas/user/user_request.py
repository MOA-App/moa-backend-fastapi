from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CreateUserRequest(BaseModel):
    """
    Payload para criação de usuário.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Sophia Sussa",
                "email": "sophia@email.com",
                "password": "Senha@123",
            }
        }
    )

    name: str = Field(
        ...,
        min_length=3,
        max_length=150,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=255,
    )


class UpdateUserRequest(BaseModel):
    """
    Payload para atualização de usuário.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Sophia Campos",
                "email": "novo@email.com",
            }
        }
    )

    name: str | None = Field(
        default=None,
        min_length=3,
        max_length=150,
    )

    email: EmailStr | None = None


class ChangePasswordRequest(BaseModel):
    """
    Payload para troca de senha.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "current_password": "Senha@123",
                "new_password": "NovaSenha@123",
            }
        }
    )

    current_password: str

    new_password: str = Field(
        ...,
        min_length=8,
        max_length=255,
    )


class AssignRoleRequest(BaseModel):
    """
    Payload para adicionar uma role ao usuário.
    """

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "role_id": "2a5a3d54-59be-4bd6-a7de-f5bb0a7e0e7c"
            }
        }
    )

    role_id: str

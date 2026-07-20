from typing import Optional, List

from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError, SQLAlchemyError, DBAPIError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.auth.domain.entities.user_entity import User
from app.modules.auth.domain.repositories.user_repository import (
    UserRepositoryInterface,
)
from app.modules.auth.domain.value_objects.user_vo.user_email_vo import Email
from app.modules.auth.domain.value_objects.user_vo.user_name_vo import UserName

from app.modules.auth.infrastructure.exceptions.repository_exception import DatabaseConnectionException, DatabaseOperationException, RepositoryException
from app.shared.domain.value_objects.id_vo import EntityId

from ..models.user_model import UserModel
from ..models.role_model import RoleModel
from ..mappers.user_mapper import UserMapper



class UserRepositoryImpl(UserRepositoryInterface):

    def __init__(self, session: AsyncSession):
        self.session = session

    # ============================================================
    # CREATE
    # ============================================================

    async def create(self, user: User) -> User:

        model = UserMapper.to_model(user)

        try:

            if user.roles:

                roles = []

                for role in user.roles:
                    role_model = await self.session.get(
                        RoleModel,
                        role.id.value,
                    )

                    if role_model:
                        roles.append(role_model)

                model.roles = roles

            self.session.add(model)

            await self.session.commit()
            await self.session.refresh(model)

            return UserMapper.to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="criar usuário",
                details=str(e.orig or e),
            )

        except (DBAPIError, ConnectionError) as e:
            await self.session.rollback()
            raise DatabaseConnectionException(
                operation="criar usuário",
                details=str(e),
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryException(
                operation="criar usuário",
                details=str(e),
            )

    # ============================================================
    # UPDATE
    # ============================================================

    async def update(self, user: User) -> User:

        model = await self.session.get(UserModel, user.id.value)

        if model is None:
            raise RepositoryException(
                operation="atualizar usuário",
                details="Usuário não encontrado.",
            )

        try:

            UserMapper.update_model_from_entity(model, user)

            model.roles.clear()

            for role in user.roles:

                role_model = await self.session.get(
                    RoleModel,
                    role.id.value,
                )

                if role_model:
                    model.roles.append(role_model)

            await self.session.commit()
            await self.session.refresh(model)

            return UserMapper.to_entity(model)

        except IntegrityError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="atualizar usuário",
                details=str(e.orig or e),
            )

        except (DBAPIError, ConnectionError) as e:
            await self.session.rollback()
            raise DatabaseConnectionException(
                operation="atualizar usuário",
                details=str(e),
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryException(
                operation="atualizar usuário",
                details=str(e),
            )

    # ============================================================
    # DELETE
    # ============================================================

    async def delete(self, user_id: EntityId) -> bool:

        try:

            result = await self.session.execute(
                delete(UserModel).where(UserModel.id == user_id.value)
            )

            await self.session.commit()

            return result.rowcount > 0

        except IntegrityError as e:
            await self.session.rollback()
            raise DatabaseOperationException(
                operation="excluir usuário",
                details=str(e.orig or e),
            )

        except (DBAPIError, ConnectionError) as e:
            await self.session.rollback()
            raise DatabaseConnectionException(
                operation="excluir usuário",
                details=str(e),
            )

        except SQLAlchemyError as e:
            await self.session.rollback()
            raise RepositoryException(
                operation="excluir usuário",
                details=str(e),
            )

    # ============================================================
    # GET BY ID
    # ============================================================

    async def get_by_id(
        self,
        user_id: EntityId,
    ) -> Optional[User]:

        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.roles)
                .selectinload(RoleModel.permissions)
            )
            .where(UserModel.id == user_id.value)
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        return UserMapper.to_entity(model) if model else None

    # ============================================================
    # GET BY EMAIL
    # ============================================================

    async def get_by_email(
        self,
        email: Email,
    ) -> Optional[User]:

        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.roles)
                .selectinload(RoleModel.permissions)
            )
            .where(UserModel.email == email.value)
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        return UserMapper.to_entity(model) if model else None

    # ============================================================
    # GET BY USERNAME
    # ============================================================

    async def get_by_username(
        self,
        username: UserName,
    ) -> Optional[User]:

        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.roles)
                .selectinload(RoleModel.permissions)
            )
            .where(UserModel.name == username.value)
        )

        result = await self.session.execute(stmt)

        model = result.scalar_one_or_none()

        return UserMapper.to_entity(model) if model else None

    # ============================================================
    # GET ALL
    # ============================================================

    async def get_all(self) -> List[User]:

        stmt = (
            select(UserModel)
            .options(
                selectinload(UserModel.roles)
                .selectinload(RoleModel.permissions)
            )
            .order_by(UserModel.name)
        )

        result = await self.session.execute(stmt)

        models = result.scalars().all()

        return UserMapper.to_entities(models)

    # ============================================================
    # EXISTS
    # ============================================================

    async def exists_by_email(
        self,
        email: Email,
    ) -> bool:

        stmt = select(UserModel.id).where(
            UserModel.email == email.value
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None

    async def exists_by_id(
        self,
        user_id: EntityId,
    ) -> bool:

        stmt = select(UserModel.id).where(
            UserModel.id == user_id.value
        )

        result = await self.session.execute(stmt)

        return result.scalar_one_or_none() is not None

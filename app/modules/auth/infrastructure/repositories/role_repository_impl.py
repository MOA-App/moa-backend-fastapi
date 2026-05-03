from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.modules.auth.domain.entities.role_entity import Role
from app.modules.auth.domain.exceptions.auth_exceptions import RoleAlreadyAssignedException, RoleAlreadyExistsException, RoleNotAssignedException, RoleNotFoundException, PermissionNotFoundException
from app.modules.auth.domain.value_objects.role_name_vo import RoleName
from app.modules.auth.domain.repositories.role_repository import RoleRepository
from app.modules.auth.infrastructure.exceptions.repository_exception import RepositoryException
from app.shared.domain.value_objects.id_vo import EntityId

from app.modules.auth.infrastructure.models.role_model import RoleModel
from app.modules.auth.infrastructure.models.permission_model import PermissionModel
from app.modules.auth.infrastructure.mappers.role_mapper import RoleMapper


class RoleRepositoryImpl(RoleRepository):
    """
    Implementação concreta do RoleRepository usando SQLAlchemy + PostgreSQL.

    Adapter da camada de infraestrutura que satisfaz o Port (RoleRepository).
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    # =========================================================================
    # CREATE
    # =========================================================================

    async def create(self, role: Role) -> Role:
        """Persiste uma nova role no banco."""
        try:
            model = RoleMapper.to_model(role)
            self._session.add(model)
            await self._session.flush()
            await self._session.refresh(model)
            return RoleMapper.to_entity(model)

        except IntegrityError:
            await self._session.rollback()
            raise RoleAlreadyExistsException(
                f"Role '{role.nome.value}' já existe."
            )
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise RepositoryException(f"Erro ao criar role: {e}") from e

    # =========================================================================
    # READ
    # =========================================================================

    async def find_by_id(self, role_id: EntityId) -> Optional[Role]:
        """Busca uma role pelo ID."""
        try:
            result = await self._session.execute(
                select(RoleModel).where(RoleModel.id == role_id.value)
            )
            model = result.scalar_one_or_none()
            return RoleMapper.to_entity(model) if model else None

        except SQLAlchemyError as e:
            raise RepositoryException(f"Erro ao buscar role por ID: {e}") from e

    async def find_by_name(self, name: RoleName) -> Optional[Role]:
        """Busca uma role pelo nome."""
        try:
            result = await self._session.execute(
                select(RoleModel).where(RoleModel.nome == name.value)
            )
            model = result.scalar_one_or_none()
            return RoleMapper.to_entity(model) if model else None

        except SQLAlchemyError as e:
            raise RepositoryException(f"Erro ao buscar role por nome: {e}") from e

    async def exists_by_name(self, name: RoleName) -> bool:
        """Verifica se já existe uma role com o nome informado."""
        try:
            result = await self._session.execute(
                select(RoleModel.id).where(RoleModel.nome == name.value)
            )
            return result.scalar_one_or_none() is not None

        except SQLAlchemyError as e:
            raise RepositoryException(
                f"Erro ao verificar existência de role: {e}"
            ) from e

    async def list_all(self) -> List[Role]:
        """Lista todas as roles cadastradas."""
        try:
            result = await self._session.execute(select(RoleModel))
            models = result.scalars().all()
            return [RoleMapper.to_entity(m) for m in models]

        except SQLAlchemyError as e:
            raise RepositoryException(f"Erro ao listar roles: {e}") from e

    # =========================================================================
    # UPDATE
    # =========================================================================

    async def update(self, role: Role) -> Role:
        """Atualiza o nome de uma role existente."""
        try:
            result = await self._session.execute(
                select(RoleModel).where(RoleModel.id == role.id.value)
            )
            model = result.scalar_one_or_none()

            if model is None:
                raise RoleNotFoundException(
                    f"Role com ID '{role.id.value}' não encontrada."
                )

            model.nome = role.nome.value

            await self._session.flush()
            await self._session.refresh(model)
            return RoleMapper.to_entity(model)

        except RoleNotFoundException:
            raise
        except IntegrityError:
            await self._session.rollback()
            raise RoleAlreadyExistsException(
                f"Role '{role.nome.value}' já existe."
            )
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise RepositoryException(f"Erro ao atualizar role: {e}") from e

    # =========================================================================
    # DELETE
    # =========================================================================

    async def delete(self, role_id: EntityId) -> None:
        """Remove uma role e suas associações de permissões."""
        try:
            result = await self._session.execute(
                select(RoleModel).where(RoleModel.id == role_id.value)
            )
            model = result.scalar_one_or_none()

            if model is None:
                raise RoleNotFoundException(
                    f"Role com ID '{role_id.value}' não encontrada."
                )

            await self._session.delete(model)
            await self._session.flush()

        except RoleNotFoundException:
            raise
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise RepositoryException(f"Erro ao deletar role: {e}") from e

    # =========================================================================
    # PERMISSIONS
    # =========================================================================

    async def add_permission_to_role(
        self,
        role_id: EntityId,
        permission_id: EntityId,
    ) -> bool:
        """Associa uma permissão a uma role."""
        try:
            role_model = await self._get_role_model_or_raise(role_id)
            permission_model = await self._get_permission_model_or_raise(permission_id)

            already_linked = any(
                p.id == permission_model.id for p in role_model.permissions
            )
            if already_linked:
                raise RoleAlreadyAssignedException(
                    f"Permissão '{permission_model.nome}' já está associada "
                    f"à role '{role_model.nome}'."
                )

            role_model.permissions.append(permission_model)
            await self._session.flush()
            return True

        except (RoleNotFoundException, RoleAlreadyAssignedException):
            raise
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise RepositoryException(
                f"Erro ao associar permissão à role: {e}"
            ) from e

    async def remove_permission_from_role(
        self,
        role_id: EntityId,
        permission_id: EntityId,
    ) -> bool:
        """Remove a associação de uma permissão de uma role."""
        try:
            role_model = await self._get_role_model_or_raise(role_id)
            permission_model = await self._get_permission_model_or_raise(permission_id)

            linked = next(
                (p for p in role_model.permissions if p.id == permission_model.id),
                None,
            )
            if linked is None:
                raise RoleNotAssignedException(
                    f"Permissão '{permission_model.nome}' não está associada "
                    f"à role '{role_model.nome}'."
                )

            role_model.permissions.remove(linked)
            await self._session.flush()
            return True

        except (RoleNotFoundException, RoleNotAssignedException):
            raise
        except SQLAlchemyError as e:
            await self._session.rollback()
            raise RepositoryException(
                f"Erro ao remover permissão da role: {e}"
            ) from e

    # =========================================================================
    # PRIVATE HELPERS
    # =========================================================================

    async def _get_role_model_or_raise(self, role_id: EntityId) -> RoleModel:
        result = await self._session.execute(
            select(RoleModel).where(RoleModel.id == role_id.value)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise RoleNotFoundException(
                f"Role com ID '{role_id.value}' não encontrada."
            )
        return model

    async def _get_permission_model_or_raise(
        self, permission_id: EntityId
    ) -> PermissionModel:

        result = await self._session.execute(
            select(PermissionModel).where(PermissionModel.id == permission_id.value)
        )
        model = result.scalar_one_or_none()
        if model is None:
            raise PermissionNotFoundException(
                f"Permissão com ID '{permission_id.value}' não encontrada."
            )
        return model

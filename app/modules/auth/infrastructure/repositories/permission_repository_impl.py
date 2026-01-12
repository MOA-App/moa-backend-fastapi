from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists, func, distinct
from sqlalchemy.orm import selectinload

from ...domain.repositories.permission_repository import PermissionRepository
from ...domain.entities.permission_entity import Permission
from ...domain.value_objects.permission_name_vo import PermissionName
from ...domain.exceptions.auth_exceptions import (
    PermissionNotFoundException,
    RepositoryException
)
from app.shared.domain.value_objects.id_vo import EntityId

from ..models.user_model import PermissionModel, RoleModel, role_permissions
from ..mappers.permission_mapper import PermissionMapper

import logging

logger = logging.getLogger(__name__)


class PermissionRepositoryImpl(PermissionRepository):
    """
    Implementação do PermissionRepository usando SQLAlchemy.
    
    Responsável por:
    - Persistir e recuperar Permission entities
    - Operações de busca e listagem
    - Consultas agregadas (recursos, ações)
    """
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = PermissionMapper()
    
    async def create(self, permission: Permission) -> Permission:
        """
        Cria nova permissão no banco.
        
        Args:
            permission: Entity Permission
            
        Returns:
            Permission: Permissão criada
            
        Raises:
            RepositoryException: Erro ao persistir
        """
        try:
            model = self.mapper.to_model(permission)
            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model)
            
            logger.info(f"Permission created: {model.nome}")
            
            return self.mapper.to_entity(model)
            
        except Exception as e:
            logger.error(f"Error creating permission: {e}")
            raise RepositoryException(
                operation="criar permissão",
                details=str(e)
            )
    
    async def find_by_id(self, permission_id: EntityId) -> Optional[Permission]:
        """
        Busca permissão por ID.
        
        Args:
            permission_id: ID da permissão
            
        Returns:
            Optional[Permission]: Permissão encontrada ou None
        """
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission_id.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if model:
                logger.debug(f"Permission found by id: {permission_id}")
            
            return self.mapper.to_entity(model) if model else None
            
        except Exception as e:
            logger.error(f"Error finding permission by id: {e}")
            raise RepositoryException(
                operation="buscar permissão por ID",
                details=str(e)
            )
    
    async def find_by_name(self, name: PermissionName) -> Optional[Permission]:
        """
        Busca permissão por nome.
        
        Args:
            name: Nome da permissão (VO)
            
        Returns:
            Optional[Permission]: Permissão encontrada ou None
        """
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.nome == name.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if model:
                logger.debug(f"Permission found by name: {name.value}")
            
            return self.mapper.to_entity(model) if model else None
            
        except Exception as e:
            logger.error(f"Error finding permission by name: {e}")
            raise RepositoryException(
                operation="buscar permissão por nome",
                details=str(e)
            )
    
    async def exists_by_name(self, name: PermissionName) -> bool:
        """
        Verifica se existe permissão com o nome.
        
        Args:
            name: Nome da permissão
            
        Returns:
            bool: True se existe
        """
        try:
            stmt = select(
                exists().where(PermissionModel.nome == name.value)
            )
            result = await self.session.execute(stmt)
            return result.scalar()
            
        except Exception as e:
            logger.error(f"Error checking permission existence: {e}")
            raise RepositoryException(
                operation="verificar existência de permissão",
                details=str(e)
            )
    
    async def list_all(self) -> List[Permission]:
        """
        Lista todas as permissões.
        
        Returns:
            List[Permission]: Lista de permissões ordenadas por nome
        """
        try:
            stmt = select(PermissionModel).order_by(PermissionModel.nome)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            logger.debug(f"Listed {len(models)} permissions")
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error listing permissions: {e}")
            raise RepositoryException(
                operation="listar permissões",
                details=str(e)
            )
    
    async def list_by_resource(self, resource: str) -> List[Permission]:
        """
        Lista permissões de um recurso específico.
        
        Busca permissões que começam com "resource."
        
        Args:
            resource: Nome do recurso (ex: "users")
            
        Returns:
            List[Permission]: Permissões do recurso
        """
        try:
            resource_lower = resource.lower()
            
            # Buscar permissões que começam com "resource."
            stmt = select(PermissionModel).where(
                PermissionModel.nome.like(f"{resource_lower}.%")
            ).order_by(PermissionModel.nome)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            logger.debug(f"Found {len(models)} permissions for resource: {resource}")
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error listing permissions by resource: {e}")
            raise RepositoryException(
                operation="listar permissões por recurso",
                details=str(e)
            )
    
    async def update(self, permission: Permission) -> Permission:
        """
        Atualiza permissão existente.
        
        Args:
            permission: Entity com dados atualizados
            
        Returns:
            Permission: Permissão atualizada
            
        Raises:
            PermissionNotFoundException: Permissão não encontrada
        """
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission.id.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                raise PermissionNotFoundException(str(permission.id.value))
            
            # Atualizar model com dados da entity
            self.mapper.update_model_from_entity(model, permission)
            
            await self.session.flush()
            await self.session.refresh(model)
            
            logger.info(f"Permission updated: {model.nome}")
            
            return self.mapper.to_entity(model)
            
        except PermissionNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating permission: {e}")
            raise RepositoryException(
                operation="atualizar permissão",
                details=str(e)
            )
    
    async def delete(self, permission_id: EntityId) -> None:
        """
        Deleta permissão.
        
        Args:
            permission_id: ID da permissão
            
        Raises:
            PermissionNotFoundException: Permissão não encontrada
        """
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission_id.value
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                raise PermissionNotFoundException(str(permission_id.value))
            
            permission_name = model.nome
            
            await self.session.delete(model)
            await self.session.flush()
            
            logger.info(f"Permission deleted: {permission_name}")
            
        except PermissionNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error deleting permission: {e}")
            raise RepositoryException(
                operation="deletar permissão",
                details=str(e)
            )
    
    async def find_by_names(self, names: List[PermissionName]) -> List[Permission]:
        """
        Busca múltiplas permissões por nome (bulk).
        
        Args:
            names: Lista de nomes de permissões
            
        Returns:
            List[Permission]: Permissões encontradas
        """
        try:
            if not names:
                return []
            
            name_values = [name.value for name in names]
            
            stmt = select(PermissionModel).where(
                PermissionModel.nome.in_(name_values)
            ).order_by(PermissionModel.nome)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            logger.debug(f"Found {len(models)} permissions from {len(names)} names")
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error finding permissions by names: {e}")
            raise RepositoryException(
                operation="buscar permissões por nomes",
                details=str(e)
            )
    
    async def count(self) -> int:
        """
        Conta total de permissões.
        
        Returns:
            int: Quantidade total
        """
        try:
            stmt = select(func.count()).select_from(PermissionModel)
            result = await self.session.execute(stmt)
            return result.scalar()
            
        except Exception as e:
            logger.error(f"Error counting permissions: {e}")
            raise RepositoryException(
                operation="contar permissões",
                details=str(e)
            )
    
    async def count_by_resource(self, resource: str) -> int:
        """
        Conta permissões de um recurso.
        
        Args:
            resource: Nome do recurso
            
        Returns:
            int: Quantidade de permissões do recurso
        """
        try:
            resource_lower = resource.lower()
            
            stmt = select(func.count()).select_from(PermissionModel).where(
                PermissionModel.nome.like(f"{resource_lower}.%")
            )
            
            result = await self.session.execute(stmt)
            return result.scalar()
            
        except Exception as e:
            logger.error(f"Error counting permissions by resource: {e}")
            raise RepositoryException(
                operation="contar permissões por recurso",
                details=str(e)
            )
    
    async def list_resources(self) -> List[str]:
        """
        Lista todos os recursos únicos que possuem permissões.
        
        Extrai a primeira parte de cada permissão (antes do primeiro ponto).
        
        Returns:
            List[str]: Lista de recursos únicos ordenados
            
        Example:
            permissions: users.create, users.read, posts.create
            result: ['posts', 'users']
        """
        try:
            # Buscar todos os nomes de permissões
            stmt = select(PermissionModel.nome)
            result = await self.session.execute(stmt)
            names = result.scalars().all()
            
            # Extrair recursos únicos (primeira parte antes do ponto)
            resources = set()
            for name in names:
                parts = name.split(".")
                if len(parts) >= 2:
                    # Se tem múltiplos níveis, pegar a primeira parte
                    # users.create -> users
                    # admin.users.create -> admin
                    resources.add(parts[0])
            
            result_list = sorted(list(resources))
            logger.debug(f"Found {len(result_list)} unique resources")
            
            return result_list
            
        except Exception as e:
            logger.error(f"Error listing resources: {e}")
            raise RepositoryException(
                operation="listar recursos",
                details=str(e)
            )
    
    async def list_actions(self, resource: str) -> List[str]:
        """
        Lista todas as ações disponíveis para um recurso.
        
        Args:
            resource: Nome do recurso
            
        Returns:
            List[str]: Lista de ações únicas ordenadas
            
        Example:
            resource: "users"
            permissions: users.create, users.read, users.update
            result: ['create', 'read', 'update']
        """
        try:
            resource_lower = resource.lower()
            
            # Buscar permissões do recurso
            stmt = select(PermissionModel.nome).where(
                PermissionModel.nome.like(f"{resource_lower}.%")
            )
            
            result = await self.session.execute(stmt)
            names = result.scalars().all()
            
            # Extrair ações (última parte após o ponto)
            actions = set()
            for name in names:
                parts = name.split(".")
                if len(parts) >= 2:
                    # users.create -> create
                    # admin.users.create -> create
                    actions.add(parts[-1])
            
            result_list = sorted(list(actions))
            logger.debug(f"Found {len(result_list)} actions for resource: {resource}")
            
            return result_list
            
        except Exception as e:
            logger.error(f"Error listing actions: {e}")
            raise RepositoryException(
                operation="listar ações",
                details=str(e)
            )
    
    async def count_roles_with_permission(self, permission_id: EntityId) -> int:
        """
        Conta quantas roles possuem esta permissão.
        
        Args:
            permission_id: ID da permissão
            
        Returns:
            int: Quantidade de roles
        """
        try:
            stmt = select(func.count()).select_from(role_permissions).where(
                role_permissions.c.permission_id == permission_id.value
            )
            
            result = await self.session.execute(stmt)
            return result.scalar()
            
        except Exception as e:
            logger.error(f"Error counting roles with permission: {e}")
            raise RepositoryException(
                operation="contar roles com permissão",
                details=str(e)
            )
    
    async def find_most_used(self, limit: int = 10) -> List[Permission]:
        """
        Encontra permissões mais usadas (mais roles possuem).
        
        Args:
            limit: Quantidade máxima a retornar
            
        Returns:
            List[Permission]: Permissões mais usadas
        """
        try:
            # Subquery para contar roles por permissão
            subq = (
                select(
                    role_permissions.c.permission_id,
                    func.count().label('role_count')
                )
                .group_by(role_permissions.c.permission_id)
                .subquery()
            )
            
            # Buscar permissões ordenadas por uso
            stmt = (
                select(PermissionModel)
                .join(subq, PermissionModel.id == subq.c.permission_id)
                .order_by(subq.c.role_count.desc())
                .limit(limit)
            )
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            logger.error(f"Error finding most used permissions: {e}")
            raise RepositoryException(
                operation="buscar permissões mais usadas",
                details=str(e)
            )

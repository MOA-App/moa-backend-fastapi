from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, exists

from ...domain.repositories.permission_repository import PermissionRepository
from ...domain.entities.permission_entity import Permission
from ...domain.value_objects.permission_name_vo import PermissionName
from ...domain.exceptions.auth_exceptions import RepositoryException, UserNotFoundException
from app.shared.domain.value_objects.id_vo import EntityId

from ..models.user_model import PermissionModel
from ..mappers.user_mapper import PermissionMapper


class PermissionRepositoryImpl(PermissionRepository):
    """Implementação do PermissionRepository usando SQLAlchemy"""
    
    def __init__(self, session: AsyncSession):
        self.session = session
        self.mapper = PermissionMapper()
    
    async def create(self, permission: Permission) -> Permission:
        """Cria uma nova permissão"""
        try:
            model = self.mapper.to_model(permission)
            self.session.add(model)
            await self.session.flush()
            await self.session.refresh(model)
            
            return self.mapper.to_entity(model)
            
        except Exception as e:
            raise RepositoryException(
                operation="criar permissão",
                details=str(e)
            )
    
    async def find_by_id(self, permission_id: EntityId) -> Optional[Permission]:
        """Busca permissão por ID"""
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission_id.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            return self.mapper.to_entity(model) if model else None
            
        except Exception as e:
            raise RepositoryException(
                operation="buscar permissão por ID",
                details=str(e)
            )
    
    async def find_by_name(self, name: PermissionName) -> Optional[Permission]:
        """Busca permissão por nome"""
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.nome == name.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            return self.mapper.to_entity(model) if model else None
            
        except Exception as e:
            raise RepositoryException(
                operation="buscar permissão por nome",
                details=str(e)
            )
    
    async def exists_by_name(self, name: PermissionName) -> bool:
        """Verifica se existe permissão com o nome informado"""
        try:
            stmt = select(
                exists().where(PermissionModel.nome == name.value)
            )
            result = await self.session.execute(stmt)
            return result.scalar()
            
        except Exception as e:
            raise RepositoryException(
                operation="verificar existência de permissão",
                details=str(e)
            )
    
    async def list_all(self) -> List[Permission]:
        """Lista todas as permissões"""
        try:
            stmt = select(PermissionModel).order_by(PermissionModel.nome)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            raise RepositoryException(
                operation="listar permissões",
                details=str(e)
            )
    
    async def list_by_resource(self, resource: str) -> List[Permission]:
        """Lista permissões por recurso"""
        try:
            # Buscar permissões que começam com "resource."
            stmt = select(PermissionModel).where(
                PermissionModel.nome.like(f"{resource.lower()}.%")
            ).order_by(PermissionModel.nome)
            
            result = await self.session.execute(stmt)
            models = result.scalars().all()
            
            return [self.mapper.to_entity(model) for model in models]
            
        except Exception as e:
            raise RepositoryException(
                operation="listar permissões por recurso",
                details=str(e)
            )
    
    async def update(self, permission: Permission) -> Permission:
        """Atualiza uma permissão"""
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission.id.value
            )
            
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                raise UserNotFoundException(str(permission.id.value))
            
            self.mapper.update_model_from_entity(model, permission)
            
            await self.session.flush()
            await self.session.refresh(model)
            
            return self.mapper.to_entity(model)
            
        except Exception as e:
            raise RepositoryException(
                operation="atualizar permissão",
                details=str(e)
            )
    
    async def delete(self, permission_id: EntityId) -> bool:
        """Deleta uma permissão"""
        try:
            stmt = select(PermissionModel).where(
                PermissionModel.id == permission_id.value
            )
            result = await self.session.execute(stmt)
            model = result.scalar_one_or_none()
            
            if not model:
                return False
            
            await self.session.delete(model)
            await self.session.flush()
            
            return True
            
        except Exception as e:
            raise RepositoryException(
                operation="deletar permissão",
                details=str(e)
            )

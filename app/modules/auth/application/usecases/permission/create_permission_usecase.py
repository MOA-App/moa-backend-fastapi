from typing import Optional

from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.entities.permission_entity import Permission
from ....domain.value_objects.permission_name_vo import PermissionName
from ....domain.exceptions.auth_exceptions import (
    PermissionAlreadyExistsException,
    DomainValidationException,
    RepositoryException
)

from ..dtos.permission_dto import CreatePermissionDTO, PermissionResponseDTO


class CreatePermissionUseCase:
    """
    Caso de uso para criar nova permissão.
    
    Responsabilidades:
    1. Validar dados através do PermissionName VO
    2. Verificar se permissão já existe
    3. Criar entidade Permission
    4. Persistir no repositório
    5. Retornar DTO de resposta
    """
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(self, dto: CreatePermissionDTO) -> PermissionResponseDTO:
        """
        Executa criação de permissão.
        
        Args:
            dto: Dados da permissão a criar
            
        Returns:
            PermissionResponseDTO: Permissão criada
            
        Raises:
            PermissionAlreadyExistsException: Permissão já existe
            DomainValidationException: Dados inválidos
            RepositoryException: Erro ao persistir
        """
        
        # 1. Validar através do Value Object
        try:
            permission_name = PermissionName(dto.nome)
        except ValueError as e:
            raise DomainValidationException(str(e))
        
        # 2. Verificar se já existe
        existing = await self.permission_repository.find_by_name(permission_name)
        if existing:
            raise PermissionAlreadyExistsException(permission_name.value)
        
        # 3. Criar entidade
        permission = Permission.create(
            nome=dto.nome,
            descricao=dto.descricao
        )
        
        # 4. Persistir
        try:
            created = await self.permission_repository.create(permission)
        except Exception as e:
            raise RepositoryException(
                operation="criar permissão",
                details=str(e)
            )
        
        # 5. Retornar DTO
        return self._to_response_dto(created)
    
    def _to_response_dto(self, permission: Permission) -> PermissionResponseDTO:
        """Converte Entity para DTO de resposta"""
        return PermissionResponseDTO(
            id=permission.id.value,
            nome=permission.nome.value,
            descricao=permission.descricao,
            data_criacao=permission.data_criacao,
            resource=permission.get_resource(),
            action=permission.get_action()
        )

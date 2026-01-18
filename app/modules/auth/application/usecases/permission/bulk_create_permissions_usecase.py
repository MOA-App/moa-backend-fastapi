from typing import List

from app.modules.auth.application.dtos.permission.permission_bulk import BulkCreatePermissionsDTO
from app.modules.auth.application.dtos.permission.permission_outputs import PermissionResponseDTO
from app.modules.auth.application.dtos.permission.permission_queries import BulkCreatePermissionsResponseDTO
from app.modules.auth.domain.exceptions.auth_exceptions import DomainValidationException, PermissionAlreadyExistsException, RepositoryException

from ....domain.repositories.permission_repository import PermissionRepository
from ....domain.entities.permission_entity import Permission
from ....domain.value_objects.permission_name_vo import PermissionName


class BulkCreatePermissionsUseCase:
    """Caso de uso para criar múltiplas permissões de uma vez"""
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(
        self,
        dto: BulkCreatePermissionsDTO
    ) -> BulkCreatePermissionsResponseDTO:
        """
        Cria múltiplas permissões em lote.
        
        Continua mesmo se algumas falharem.
        Retorna criadas, ignoradas e erros.
        """
        created: List[PermissionResponseDTO] = []
        skipped: List[str] = []
        errors: List[dict] = []
        
        for perm_dto in dto.permissions:
            try:
                # Validar
                permission_name = PermissionName(perm_dto.nome)
                
                # Verificar se já existe
                existing = await self.permission_repository.find_by_name(
                    permission_name
                )
                
                if existing:
                    skipped.append(perm_dto.nome)
                    continue
                
                # Criar
                permission = Permission.create(
                    nome=perm_dto.nome,
                    descricao=perm_dto.descricao
                )
                
                saved = await self.permission_repository.create(permission)
                
                created.append(
                    PermissionResponseDTO(
                        id=saved.id.value,
                        nome=saved.nome.value,
                        descricao=saved.descricao,
                        data_criacao=saved.data_criacao,
                        resource=saved.get_resource(),
                        action=saved.get_action()
                    )
                )
                
            except DomainValidationException as e:
                errors.append({"nome": perm_dto.nome, "error": str(e)})
            except PermissionAlreadyExistsException:
                skipped.append(perm_dto.nome)
            except RepositoryException as e:
                errors.append({"nome": perm_dto.nome, "error": "Erro interno"})
                    
        return BulkCreatePermissionsResponseDTO(
            created=created,
            skipped=skipped,
            errors=errors,
            total_created=len(created),
            total_skipped=len(skipped),
            total_errors=len(errors)
        )

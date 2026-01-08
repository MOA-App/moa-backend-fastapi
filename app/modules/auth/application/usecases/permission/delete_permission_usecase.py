class DeletePermissionUseCase:
    """Caso de uso para deletar permissão"""
    
    def __init__(self, permission_repository: PermissionRepository):
        self.permission_repository = permission_repository
    
    async def execute(self, permission_id: str) -> bool:
        """
        Deleta permissão por ID.
        
        Args:
            permission_id: UUID da permissão
            
        Returns:
            bool: True se deletado com sucesso
            
        Raises:
            PermissionNotFoundException: Permissão não encontrada
        """
        try:
            entity_id = EntityId.from_string(permission_id)
        except ValueError:
            raise PermissionNotFoundException(permission_id)
        
        try:
            # Verificar se existe
            permission = await self.permission_repository.find_by_id(entity_id)
            if not permission:
                raise PermissionNotFoundException(permission_id)
            
            # Deletar
            await self.permission_repository.delete(entity_id)
            return True
            
        except PermissionNotFoundException:
            raise
        except Exception as e:
            raise RepositoryException(
                operation="deletar permissão",
                details=str(e)
            )

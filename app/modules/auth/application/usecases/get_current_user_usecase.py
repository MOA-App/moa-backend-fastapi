from ...domain.repositories.user_repository import UserRepository
from ...domain.exceptions.auth_exceptions import UserNotFoundException
from ..dtos.user_response_dto import UserResponseDTO, RoleResponseDTO, PermissionResponseDTO
from app.shared.domain.value_objects.id_vo import EntityId


class GetCurrentUserUseCase:
    """
    Caso de uso para obter dados do usuário autenticado.
    """
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    async def execute(self, user_id: str) -> UserResponseDTO:
        """
        Obtém dados completos do usuário atual.
        
        Args:
            user_id: ID do usuário (string UUID)
            
        Returns:
            UserResponseDTO: Dados do usuário
            
        Raises:
            UserNotFoundException: Usuário não encontrado
        """
        try:
            entity_id = EntityId.from_string(user_id)
        except ValueError:
            raise UserNotFoundException(user_id)
        
        user = await self.user_repository.find_by_id(entity_id)
        
        if not user:
            raise UserNotFoundException(user_id)
        
        return UserResponseDTO(
            id=user.id.value,
            nome=user.nome.value,
            email=user.email.value,
            nome_usuario=user.nome_usuario.value,
            data_cadastro=user.data_cadastro,
            roles=[
                RoleResponseDTO(
                    id=role.id.value,
                    nome=role.nome.value,
                    permissions=[
                        PermissionResponseDTO(
                            id=perm.id.value,
                            nome=perm.nome.value,
                            descricao=perm.descricao,
                            data_criacao=perm.data_criacao
                        )
                        for perm in role.permissions
                    ]
                )
                for role in user.roles
            ],
            enderecos=[]
        )

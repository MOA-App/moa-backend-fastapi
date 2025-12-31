from typing import Optional

from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user_entity import User
from ...domain.value_objects.email_vo import Email
from ...domain.value_objects.password_vo import Password
from ...domain.value_objects.username_vo import Username
from ...domain.value_objects.person_name_vo import PersonName
from ...domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    DomainValidationException,
    RepositoryException
)
from ...infrastructure.security.password_hasher import PasswordHasher
from ..dtos.register_dto import RegisterDTO
from ..dtos.user_response_dto import UserResponseDTO, RoleResponseDTO, PermissionResponseDTO


class RegisterUseCase:
    """
    Caso de uso para registro de novo usuário.
    
    Responsabilidades:
    1. Validar dados através dos Value Objects
    2. Verificar se usuário já existe (email e username)
    3. Hashear a senha
    4. Criar entidade User
    5. Persistir no repositório
    6. Retornar DTO de resposta
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
    
    async def execute(self, dto: RegisterDTO) -> UserResponseDTO:
        """
        Executa o caso de uso de registro.
        
        Args:
            dto: Dados de registro do usuário
            
        Returns:
            UserResponseDTO: Dados do usuário criado
            
        Raises:
            UserAlreadyExistsException: Email ou username já cadastrado
            DomainValidationException: Dados inválidos
            RepositoryException: Erro ao persistir dados
        """
        
        # 1. Validar dados através dos Value Objects
        try:
            email = Email(dto.email)
            username = Username(dto.nome_usuario)
            person_name = PersonName(dto.nome)
            password = Password(dto.senha)  # Valida força da senha
            
        except ValueError as e:
            raise DomainValidationException(str(e))
        
        # 2. Verificar se usuário já existe
        await self._check_user_uniqueness(email, username)
        
        # 3. Hashear a senha
        hashed_password = self.password_hasher.hash(password.value)
        
        # 4. Criar entidade User usando factory method
        user = User.create(
            nome=person_name.value,
            email=email.value,
            senha_hash=hashed_password,
            nome_usuario=username.value,
            id_token_firebase=dto.id_token_firebase
        )
        
        # 5. Persistir no repositório
        try:
            created_user = await self.user_repository.create(user)
        except Exception as e:
            raise RepositoryException(
                operation="criar usuário",
                details=str(e)
            )
        
        # 6. Retornar DTO de resposta
        return self._to_response_dto(created_user)
    
    async def _check_user_uniqueness(
        self,
        email: Email,
        username: Username
    ) -> None:
        """
        Verifica se email e username são únicos.
        
        Raises:
            UserAlreadyExistsException: Se email ou username já existir
        """
        # Verifica email
        if await self.user_repository.exists_by_email(email):
            raise UserAlreadyExistsException(
                field="email",
                value=email.value
            )
        
        # Verifica username
        if await self.user_repository.exists_by_username(username):
            raise UserAlreadyExistsException(
                field="nome de usuário",
                value=username.value
            )
    
    def _to_response_dto(self, user: User) -> UserResponseDTO:
        """
        Converte entidade User para DTO de resposta.
        
        Args:
            user: Entidade User
            
        Returns:
            UserResponseDTO: DTO de resposta
        """
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

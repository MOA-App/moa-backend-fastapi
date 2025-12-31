from datetime import timedelta

from ...domain.repositories.user_repository import UserRepository
from ...domain.entities.user_entity import User
from ...domain.value_objects.email_vo import Email
from ...domain.exceptions.auth_exceptions import (
    InvalidCredentialsException,
    DomainValidationException,
    UserInactiveException
)
from ...infrastructure.security.password_hasher import PasswordHasher
from ...infrastructure.security.jwt_handler import JWTHandler
from ..dtos.login_dto import LoginDTO
from ..dtos.token_dto import TokenDTO
from ..dtos.user_response_dto import UserResponseDTO, RoleResponseDTO, PermissionResponseDTO


class LoginUseCase:
    """
    Caso de uso para autenticação de usuário.
    
    Responsabilidades:
    1. Validar email
    2. Buscar usuário no repositório
    3. Verificar senha
    4. Verificar se usuário está ativo
    5. Gerar token JWT
    6. Retornar token e dados do usuário
    """
    
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher: PasswordHasher,
        jwt_handler: JWTHandler
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.jwt_handler = jwt_handler
    
    async def execute(self, dto: LoginDTO) -> TokenDTO:
        """
        Executa o caso de uso de login.
        
        Args:
            dto: Dados de login (email e senha)
            
        Returns:
            TokenDTO: Token JWT e dados do usuário
            
        Raises:
            InvalidCredentialsException: Email ou senha incorretos
            DomainValidationException: Email inválido
            UserInactiveException: Usuário inativo
        """
        
        # 1. Validar email
        try:
            email = Email(dto.email)
        except ValueError as e:
            raise DomainValidationException(str(e))
        
        # 2. Buscar usuário
        user = await self._find_user_by_email(email)
        
        # 3. Verificar senha
        self._verify_password(dto.senha, user.senha.value)
        
        # 4. Verificar se usuário está ativo
        self._check_user_active(user)
        
        # 5. Gerar token JWT
        access_token = self._generate_access_token(user)
        
        # 6. Retornar resposta com token
        return TokenDTO(
            access_token=access_token,
            token_type="bearer",
            expires_in=self.jwt_handler.access_token_expire_minutes * 60,
            user=self._to_user_response_dto(user)
        )
    
    async def _find_user_by_email(self, email: Email) -> User:
        """
        Busca usuário por email.
        
        Args:
            email: Email do usuário
            
        Returns:
            User: Usuário encontrado
            
        Raises:
            InvalidCredentialsException: Usuário não encontrado
        """
        user = await self.user_repository.find_by_email(email)
        
        if not user:
            # Não revela se o email existe ou não por segurança
            raise InvalidCredentialsException()
        
        return user
    
    def _verify_password(self, plain_password: str, hashed_password: str) -> None:
        """
        Verifica se a senha está correta.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Senha hasheada armazenada
            
        Raises:
            InvalidCredentialsException: Senha incorreta
        """
        is_valid = self.password_hasher.verify(plain_password, hashed_password)
        
        if not is_valid:
            raise InvalidCredentialsException()
    
    def _check_user_active(self, user: User) -> None:
        """
        Verifica se o usuário está ativo.
        
        Args:
            user: Usuário a verificar
            
        Raises:
            UserInactiveException: Usuário inativo
        """
        if not user.is_active():
            raise UserInactiveException()
    
    def _generate_access_token(self, user: User) -> str:
        """
        Gera token JWT para o usuário.
        
        Args:
            user: Usuário autenticado
            
        Returns:
            str: Token JWT
        """
        token_data = {
            "sub": str(user.id.value),
            "email": user.email.value,
            "username": user.nome_usuario.value,
            "roles": user.get_roles(),
            "permissions": user.get_all_permissions()
        }
        
        return self.jwt_handler.create_access_token(data=token_data)
    
    def _to_user_response_dto(self, user: User) -> UserResponseDTO:
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

"""
Exceções do Domínio de Autenticação.
Estas exceções representam regras de negócio violadas.
"""


class AuthException(Exception):
    """Exceção base para o módulo de autenticação"""
    def __init__(self, message: str = "Erro de autenticação"):
        self.message = message
        super().__init__(self.message)


class DomainValidationException(AuthException):
    """Exceção base para erros de validação de domínio"""
    def __init__(self, message: str = "Erro de validação"):
        super().__init__(message)


# ============================================================================
# USER EXCEPTIONS
# ============================================================================

class UserException(AuthException):
    """Exceção base para erros relacionados a usuários"""
    pass


class UserAlreadyExistsException(UserException):
    """Usuário já existe no sistema"""
    def __init__(self, field: str, value: str):
        message = f"Usuário com {field} '{value}' já existe"
        super().__init__(message)


class UserNotFoundException(UserException):
    """Usuário não encontrado"""
    def __init__(self, identifier: str = "ID"):
        message = f"Usuário não encontrado: {identifier}"
        super().__init__(message)


class UserInactiveException(UserException):
    """Usuário está inativo"""
    def __init__(self):
        super().__init__("Usuário está inativo")


class InvalidUserDataException(UserException):
    """Dados do usuário são inválidos"""
    def __init__(self, message: str):
        super().__init__(f"Dados inválidos: {message}")


# ============================================================================
# AUTHENTICATION EXCEPTIONS
# ============================================================================

class AuthenticationException(AuthException):
    """Exceção base para erros de autenticação"""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Credenciais inválidas fornecidas"""
    def __init__(self):
        super().__init__("Email ou senha incorretos")


class InvalidTokenException(AuthenticationException):
    """Token JWT inválido"""
    def __init__(self, reason: str = "Token inválido"):
        super().__init__(reason)


class TokenExpiredException(AuthenticationException):
    """Token JWT expirado"""
    def __init__(self):
        super().__init__("Token expirado. Faça login novamente")


class TokenNotFoundException(AuthenticationException):
    """Token não fornecido"""
    def __init__(self):
        super().__init__("Token de autenticação não fornecido")


# ============================================================================
# AUTHORIZATION EXCEPTIONS
# ============================================================================

class AuthorizationException(AuthException):
    """Exceção base para erros de autorização"""
    pass


class UnauthorizedException(AuthorizationException):
    """Usuário não autorizado para realizar a ação"""
    def __init__(self, action: str = "esta ação"):
        super().__init__(f"Você não tem permissão para {action}")


class InsufficientPermissionsException(AuthorizationException):
    """Usuário não possui as permissões necessárias"""
    def __init__(self, permission: str):
        message = f"Permissão necessária: {permission}"
        super().__init__(message)


class RoleNotFoundException(AuthorizationException):
    """Role não encontrada"""
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' não encontrada")


# ============================================================================
# PERMISSION EXCEPTIONS
# ============================================================================

class PermissionException(AuthException):
    """Exceção base para erros de permissão"""
    pass


class PermissionAlreadyExistsException(PermissionException):
    """Permissão já existe"""
    def __init__(self, permission_name: str):
        super().__init__(f"Permissão '{permission_name}' já existe")


class PermissionNotFoundException(PermissionException):
    """Permissão não encontrada"""
    def __init__(self, permission_name: str):
        super().__init__(f"Permissão '{permission_name}' não encontrada")


class InvalidPermissionFormatException(PermissionException):
    """Formato da permissão é inválido"""
    def __init__(self, permission_name: str):
        message = f"Formato inválido: '{permission_name}'. Use 'resource.action'"
        super().__init__(message)


# ============================================================================
# ROLE EXCEPTIONS
# ============================================================================

class RoleException(AuthException):
    """Exceção base para erros de role"""
    pass


class RoleAlreadyExistsException(RoleException):
    """Role já existe"""
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' já existe")


class RoleAlreadyAssignedException(RoleException):
    """Role já está atribuída ao usuário"""
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' já está atribuída a este usuário")


class RoleNotAssignedException(RoleException):
    """Role não está atribuída ao usuário"""
    def __init__(self, role_name: str):
        super().__init__(f"Role '{role_name}' não está atribuída a este usuário")


# ============================================================================
# REPOSITORY EXCEPTIONS
# ============================================================================

class RepositoryException(AuthException):
    """Exceção base para erros de repositório"""
    def __init__(self, message: str = "Erro ao acessar banco de dados"):
        super().__init__(message)


class DatabaseConnectionException(RepositoryException):
    """Erro de conexão com banco de dados"""
    def __init__(self):
        super().__init__("Erro ao conectar com o banco de dados")


class DatabaseOperationException(RepositoryException):
    """Erro ao executar operação no banco"""
    def __init__(self, operation: str, details: str = ""):
        message = f"Erro ao executar {operation}"
        if details:
            message += f": {details}"
        super().__init__(message)


# ============================================================================
# VALUE OBJECT EXCEPTIONS
# ============================================================================

class ValueObjectValidationException(DomainValidationException):
    """Erro de validação em Value Object"""
    def __init__(self, vo_name: str, message: str):
        super().__init__(f"{vo_name}: {message}")


class InvalidEmailException(ValueObjectValidationException):
    """Email inválido"""
    def __init__(self, email: str):
        super().__init__("Email", f"'{email}' não é um email válido")


class InvalidPasswordException(ValueObjectValidationException):
    """Senha inválida"""
    def __init__(self, reason: str):
        super().__init__("Password", reason)


class InvalidUsernameException(ValueObjectValidationException):
    """Username inválido"""
    def __init__(self, reason: str):
        super().__init__("Username", reason)


class InvalidCEPException(ValueObjectValidationException):
    """CEP inválido"""
    def __init__(self, cep: str):
        super().__init__("CEP", f"'{cep}' não é um CEP válido")

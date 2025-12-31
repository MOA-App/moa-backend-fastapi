"""
Exceções do Domínio de Autenticação.
Estas exceções representam regras de negócio violadas.
"""


class AuthException(Exception):
    """Exceção base para o módulo de autenticação"""
    pass


class DomainValidationException(AuthException):
    """Exceção base para erros de validação de domínio"""
    pass

# ============================================================================
# USER EXCEPTIONS
# ============================================================================

class UserException(AuthException):
    """Exceção base para erros relacionados a usuários"""
    pass


class UserAlreadyExistsException(UserException):
    """Usuário já existe no sistema"""
    pass


class UserNotFoundException(UserException):
    """Usuário não encontrado"""
    pass


class UserInactiveException(UserException):
    """Usuário está inativo"""
    pass

class InvalidUserDataException(UserException):
    """Dados do usuário são inválidos"""
    pass


# ============================================================================
# AUTHENTICATION EXCEPTIONS
# ============================================================================

class AuthenticationException(AuthException):
    """Exceção base para erros de autenticação"""
    pass


class InvalidCredentialsException(AuthenticationException):
    """Credenciais inválidas fornecidas"""
    pass


class InvalidTokenException(AuthenticationException):
    """Token JWT inválido"""
    pass


class TokenExpiredException(AuthenticationException):
    """Token JWT expirado"""
    pass

class TokenNotFoundException(AuthenticationException):
    """Token não fornecido"""
    pass


# ============================================================================
# AUTHORIZATION EXCEPTIONS
# ============================================================================

class AuthorizationException(AuthException):
    """Exceção base para erros de autorização"""
    pass


class UnauthorizedException(AuthorizationException):
    """Usuário não autorizado para realizar a ação"""
    pass


class InsufficientPermissionsException(AuthorizationException):
    """Usuário não possui as permissões necessárias"""
    pass

class RoleNotFoundException(AuthorizationException):
    """Role não encontrada"""
    pass


# ============================================================================
# PERMISSION EXCEPTIONS
# ============================================================================

class PermissionException(AuthException):
    """Exceção base para erros de permissão"""
    pass


class PermissionAlreadyExistsException(PermissionException):
    """Permissão já existe"""
    pass


class PermissionNotFoundException(PermissionException):
    """Permissão não encontrada"""
    pass


class InvalidPermissionFormatException(PermissionException):
    """Formato da permissão é inválido"""
    pass


# ============================================================================
# ROLE EXCEPTIONS
# ============================================================================

class RoleException(AuthException):
    """Exceção base para erros de role"""
    pass


class RoleAlreadyExistsException(RoleException):
    """Role já existe"""
    pass


class RoleAlreadyAssignedException(RoleException):
    """Role já está atribuída ao usuário"""
    pass


class RoleNotAssignedException(RoleException):
    """Role não está atribuída ao usuário"""
    pass


# ============================================================================
# REPOSITORY EXCEPTIONS
# ============================================================================

class RepositoryException(AuthException):
    """Exceção base para erros de repositório"""
    pass


class DatabaseConnectionException(RepositoryException):
    """Erro de conexão com banco de dados"""
    pass


class DatabaseOperationException(RepositoryException):
    """Erro ao executar operação no banco"""
    pass


# ============================================================================
# VALUE OBJECT EXCEPTIONS
# ============================================================================

class ValueObjectValidationException(DomainValidationException):
    """Erro de validação em Value Object"""
    pass


class InvalidEmailException(ValueObjectValidationException):
    """Email inválido"""
    pass


class InvalidPasswordException(ValueObjectValidationException):
    """Senha inválida"""
    pass


class InvalidUsernameException(ValueObjectValidationException):
    """Username inválido"""
    pass


class InvalidCEPException(ValueObjectValidationException):
    """CEP inválido"""
    pass

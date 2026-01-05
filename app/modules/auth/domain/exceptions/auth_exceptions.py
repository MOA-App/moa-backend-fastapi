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

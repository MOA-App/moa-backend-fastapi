"""
Exceções da camada Infrastructure para o módulo Category.

Essas exceções representam falhas técnicas de persistência (banco de dados,
constraints, conexão, etc). Elas NÃO são regras de negócio — isso fica nas
exceptions do domain (category_exceptions.py).

A ideia é: o repository captura erros técnicos do SQLAlchemy/driver e
re-lança como uma dessas exceptions, para que a camada de cima (use cases)
não precise conhecer detalhes do SQLAlchemy.
"""


class CategoryInfrastructureException(Exception):
    """Exceção base para erros de infraestrutura do módulo Category"""
    pass


class CategoryRepositoryException(CategoryInfrastructureException):
    """Erro genérico ao executar uma operação no repositório de categorias"""

    def __init__(self, operation: str, details: str = ""):
        self.operation = operation
        self.details = details
        message = f"Erro ao {operation} categoria no banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class CategoryDatabaseConnectionException(CategoryInfrastructureException):
    """Erro de conexão com o banco de dados ao operar sobre categorias"""

    def __init__(self, details: str = ""):
        message = "Erro de conexão com o banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class CategoryIntegrityException(CategoryInfrastructureException):
    """
    Violação de constraint no banco de dados
    (ex: nome duplicado, foreign key inválida).
    """

    def __init__(self, details: str = ""):
        message = "Violação de integridade no banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class CategoryMappingException(CategoryInfrastructureException):
    """Erro ao converter entre Model (SQLAlchemy) e Entity (domínio)"""

    def __init__(self, details: str = ""):
        message = "Erro ao converter dados da categoria"
        if details:
            message += f": {details}"
        super().__init__(message)

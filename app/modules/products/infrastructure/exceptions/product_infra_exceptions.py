"""
Exceções da camada Infrastructure para o módulo Product.

Essas exceções representam falhas técnicas de persistência (banco de dados,
constraints, conexão, etc). Elas NÃO são regras de negócio — isso fica nas
exceptions do domain (product_exceptions.py).

A ideia é: o repository captura erros técnicos do SQLAlchemy/driver e
re-lança como uma dessas exceptions, para que a camada de cima (use cases)
não precise conhecer detalhes do SQLAlchemy.
"""


class ProductInfrastructureException(Exception):
    """Exceção base para erros de infraestrutura do módulo Product"""
    pass


class ProductRepositoryException(ProductInfrastructureException):
    """Erro genérico ao executar uma operação no repositório de produtos"""

    def __init__(self, operation: str, details: str = ""):
        self.operation = operation
        self.details = details
        message = f"Erro ao {operation} produto no banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class ProductDatabaseConnectionException(ProductInfrastructureException):
    """Erro de conexão com o banco de dados ao operar sobre produtos"""

    def __init__(self, details: str = ""):
        message = "Erro de conexão com o banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class ProductIntegrityException(ProductInfrastructureException):
    """
    Violação de constraint no banco de dados
    (ex: SKU duplicado, category_id inexistente / foreign key inválida).
    """

    def __init__(self, details: str = ""):
        message = "Violação de integridade no banco de dados"
        if details:
            message += f": {details}"
        super().__init__(message)


class ProductMappingException(ProductInfrastructureException):
    """Erro ao converter entre Model (SQLAlchemy) e Entity (domínio)"""

    def __init__(self, details: str = ""):
        message = "Erro ao converter dados do produto"
        if details:
            message += f": {details}"
        super().__init__(message)

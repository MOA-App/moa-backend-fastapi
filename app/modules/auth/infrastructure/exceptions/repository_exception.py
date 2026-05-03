"""
Exceções de Infraestrutura (Persistência, Banco, ORM).
"""

class InfrastructureException(Exception):
    pass


class RepositoryException(InfrastructureException):
    def __init__(self, operation: str = "", details: str = ""):
        super().__init__(f"Erro ao {operation}: {details}")
        self.operation = operation
        self.details = details


class DatabaseConnectionException(RepositoryException):
    pass


class DatabaseOperationException(RepositoryException):
    pass

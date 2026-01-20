class CategoryNotFoundException(Exception):
    """Exceção quando categoria não é encontrada"""
    pass


class CategoryAlreadyExistsException(Exception):
    """Exceção quando categoria já existe"""
    pass


class CategoryValidationException(Exception):
    """Exceção de validação de categoria"""
    pass
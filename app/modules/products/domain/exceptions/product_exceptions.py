class ProductNotFoundException(Exception):
    """Exceção quando produto não é encontrado"""
    pass


class ProductAlreadyExistsException(Exception):
    """Exceção quando produto já existe (SKU duplicado)"""
    pass


class ProductValidationException(Exception):
    """Exceção de validação de produto"""
    pass


class ProductOutOfStockException(Exception):
    """Exceção quando produto está fora de estoque"""
    pass


class InvalidProductPriceException(Exception):
    """Exceção quando o preço do produto é inválido"""
    pass


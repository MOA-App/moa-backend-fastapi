from passlib.context import CryptContext
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class PasswordHasher:
    """
    Serviço para hash e verificação de senhas usando bcrypt.
    
    Responsabilidades:
    - Criar hash de senhas
    - Verificar senhas contra hashes
    - Gerenciar configuração do bcrypt
    """
    
    def __init__(self, rounds: int = None):
        """
        Inicializa o hasher com bcrypt.
        
        Args:
            rounds: Número de rounds do bcrypt (padrão: 12)
                   Quanto maior, mais seguro mas mais lento
        """
        self.rounds = rounds or settings.BCRYPT_ROUNDS
        
        self.pwd_context = CryptContext(
            schemes=["bcrypt"],
            deprecated="auto",
            bcrypt__rounds=self.rounds
        )
        
        logger.info(f"PasswordHasher initialized with {self.rounds} rounds")
    
    def hash(self, password: str) -> str:
        """
        Cria hash de uma senha.
        
        Args:
            password: Senha em texto plano
            
        Returns:
            str: Hash da senha (bcrypt)
            
        Example:
            >>> hasher = PasswordHasher()
            >>> hash = hasher.hash("MinhaSenh@123")
            >>> hash
            '$2b$12$abc123...'
        """
        return self.pwd_context.hash(password)
    
    def verify(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verifica se uma senha corresponde ao hash.
        
        Args:
            plain_password: Senha em texto plano
            hashed_password: Hash armazenado no banco
            
        Returns:
            bool: True se a senha está correta, False caso contrário
            
        Example:
            >>> hasher = PasswordHasher()
            >>> hash = hasher.hash("MinhaSenh@123")
            >>> hasher.verify("MinhaSenh@123", hash)
            True
            >>> hasher.verify("SenhaErrada", hash)
            False
        """
        try:
            return self.pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            logger.error(f"Error verifying password: {e}")
            return False
    
    def needs_rehash(self, hashed_password: str) -> bool:
        """
        Verifica se o hash precisa ser refeito.
        
        Útil quando você aumenta o número de rounds.
        
        Args:
            hashed_password: Hash existente
            
        Returns:
            bool: True se precisa refazer o hash
        """
        return self.pwd_context.needs_update(hashed_password)

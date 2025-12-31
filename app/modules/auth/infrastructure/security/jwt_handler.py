from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt, ExpiredSignatureError
from app.core.config import settings
from ...domain.exceptions.auth_exceptions import (
    InvalidTokenException,
    TokenExpiredException
)
import logging

logger = logging.getLogger(__name__)


class JWTHandler:
    """
    Serviço para criação e validação de tokens JWT.
    
    Responsabilidades:
    - Criar tokens de acesso
    - Decodificar e validar tokens
    - Gerenciar expiração
    """
    
    def __init__(
        self,
        secret_key: str = None,
        algorithm: str = None,
        access_token_expire_minutes: int = None
    ):
        """
        Inicializa o JWT handler.
        
        Args:
            secret_key: Chave secreta para assinar tokens
            algorithm: Algoritmo de assinatura (padrão: HS256)
            access_token_expire_minutes: Tempo de expiração em minutos
        """
        self.secret_key = secret_key or settings.SECRET_KEY
        self.algorithm = algorithm or settings.ALGORITHM
        self.access_token_expire_minutes = (
            access_token_expire_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        
        if not self.secret_key or self.secret_key == "your-secret-key-change-in-production-please":
            logger.warning("⚠️  Using default SECRET_KEY! Change in production!")
    
    def create_access_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria um token JWT de acesso.
        
        Args:
            data: Dados a serem codificados no token (payload)
            expires_delta: Tempo customizado de expiração (opcional)
            
        Returns:
            str: Token JWT assinado
            
        Example:
            >>> handler = JWTHandler()
            >>> token = handler.create_access_token({
            ...     "sub": "user-uuid",
            ...     "email": "user@example.com"
            ... })
        """
        to_encode = data.copy()
        
        # Calcular expiração
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=self.access_token_expire_minutes
            )
        
        # Adicionar claims padrão
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),  # Issued at
            "type": "access"
        })
        
        # Criar token
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        logger.debug(f"Created JWT token for subject: {data.get('sub', 'unknown')}")
        
        return encoded_jwt
    
    def create_refresh_token(
        self,
        data: Dict[str, Any],
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Cria um token JWT de refresh.
        
        Args:
            data: Dados a serem codificados
            expires_delta: Tempo de expiração (padrão: 7 dias)
            
        Returns:
            str: Refresh token JWT
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                days=settings.REFRESH_TOKEN_EXPIRE_DAYS
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        })
        
        encoded_jwt = jwt.encode(
            to_encode,
            self.secret_key,
            algorithm=self.algorithm
        )
        
        return encoded_jwt
    
    def decode_token(self, token: str) -> Dict[str, Any]:
        """
        Decodifica e valida um token JWT.
        
        Args:
            token: Token JWT a ser decodificado
            
        Returns:
            Dict[str, Any]: Payload do token
            
        Raises:
            TokenExpiredException: Token expirado
            InvalidTokenException: Token inválido
            
        Example:
            >>> handler = JWTHandler()
            >>> token = handler.create_access_token({"sub": "user-123"})
            >>> payload = handler.decode_token(token)
            >>> payload["sub"]
            'user-123'
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # Verificar tipo de token (opcional)
            token_type = payload.get("type")
            if token_type and token_type != "access":
                raise InvalidTokenException("Token type mismatch")
            
            return payload
            
        except ExpiredSignatureError:
            logger.warning("JWT token expired")
            raise TokenExpiredException()
            
        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            raise InvalidTokenException(f"Token inválido: {str(e)}")
    
    def decode_refresh_token(self, token: str) -> Dict[str, Any]:
        """
        Decodifica um refresh token.
        
        Args:
            token: Refresh token JWT
            
        Returns:
            Dict[str, Any]: Payload do token
            
        Raises:
            InvalidTokenException: Token inválido ou não é refresh token
        """
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            
            # Verificar se é refresh token
            if payload.get("type") != "refresh":
                raise InvalidTokenException("Not a refresh token")
            
            return payload
            
        except ExpiredSignatureError:
            raise TokenExpiredException()
        except JWTError as e:
            raise InvalidTokenException(f"Token inválido: {str(e)}")
    
    def get_token_expiration(self, token: str) -> Optional[datetime]:
        """
        Retorna a data de expiração de um token.
        
        Args:
            token: Token JWT
            
        Returns:
            Optional[datetime]: Data de expiração ou None se inválido
        """
        try:
            payload = self.decode_token(token)
            exp_timestamp = payload.get("exp")
            
            if exp_timestamp:
                return datetime.fromtimestamp(exp_timestamp)
            
            return None
            
        except (TokenExpiredException, InvalidTokenException):
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """
        Verifica se um token está expirado.
        
        Args:
            token: Token JWT
            
        Returns:
            bool: True se expirado, False caso contrário
        """
        try:
            self.decode_token(token)
            return False
        except TokenExpiredException:
            return True
        except InvalidTokenException:
            return True

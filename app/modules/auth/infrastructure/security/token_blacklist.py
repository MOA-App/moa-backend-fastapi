from typing import Set
from datetime import datetime, timedelta
import asyncio
import logging

logger = logging.getLogger(__name__)


class TokenBlacklist:
    """
    Blacklist simples de tokens em memória.
    
    Para produção, use Redis ou similar.
    
    Útil para logout: adiciona token na blacklist para invalidá-lo.
    """
    
    def __init__(self):
        self._blacklist: Set[str] = set()
        self._cleanup_interval = 3600  # 1 hora
        
    async def add(self, token: str, expires_at: datetime) -> None:
        """Adiciona token à blacklist"""
        self._blacklist.add(token)
        logger.info(f"Token added to blacklist (total: {len(self._blacklist)})")
    
    async def is_blacklisted(self, token: str) -> bool:
        """Verifica se token está na blacklist"""
        return token in self._blacklist
    
    async def remove(self, token: str) -> None:
        """Remove token da blacklist"""
        self._blacklist.discard(token)
    
    async def cleanup_expired(self) -> None:
        """Remove tokens expirados da blacklist (implementação simples)"""
        # Em produção, armazenar timestamp junto com token
        # e remover baseado em expiração
        pass
    
    def size(self) -> int:
        """Retorna tamanho da blacklist"""
        return len(self._blacklist)

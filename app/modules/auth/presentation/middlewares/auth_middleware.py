from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable
import time
import logging

logger = logging.getLogger(__name__)


class AuthLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware para logging de requisições de autenticação.
    """
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Log da requisição
        start_time = time.time()
        
        logger.info(
            f"Auth Request: {request.method} {request.url.path} "
            f"from {request.client.host if request.client else 'unknown'}"
        )
        
        # Processar requisição
        try:
            response = await call_next(request)
            
            # Log da resposta
            process_time = time.time() - start_time
            logger.info(
                f"Auth Response: {request.method} {request.url.path} "
                f"status={response.status_code} time={process_time:.3f}s"
            )
            
            return response
            
        except Exception as e:
            logger.error(
                f"Auth Error: {request.method} {request.url.path} "
                f"error={str(e)}"
            )
            raise


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware para rate limiting em endpoints de autenticação.
    Previne brute force attacks.
    """
    
    def __init__(self, app, max_requests: int = 5, window_seconds: int = 60):
        super().__init__(app)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = {}  # {ip: [(timestamp, endpoint), ...]}
    
    async def dispatch(self, request: Request, call_next: Callable):
        # Apenas para endpoints sensíveis
        if request.url.path in ["/auth/login", "/auth/register"]:
            client_ip = request.client.host if request.client else "unknown"
            
            # Verificar rate limit
            if self._is_rate_limited(client_ip, request.url.path):
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={
                        "error": "rate_limit_exceeded",
                        "message": "Muitas tentativas. Tente novamente mais tarde."
                    }
                )
            
            # Registrar requisição
            self._record_request(client_ip, request.url.path)
        
        return await call_next(request)
    
    def _is_rate_limited(self, ip: str, endpoint: str) -> bool:
        """Verifica se IP atingiu o limite de requisições"""
        current_time = time.time()
        
        if ip not in self.requests:
            return False
        
        # Filtrar requisições dentro da janela de tempo
        recent_requests = [
            (ts, ep) for ts, ep in self.requests[ip]
            if current_time - ts < self.window_seconds and ep == endpoint
        ]
        
        self.requests[ip] = recent_requests
        
        return len(recent_requests) >= self.max_requests
    
    def _record_request(self, ip: str, endpoint: str) -> None:
        """Registra uma nova requisição"""
        if ip not in self.requests:
            self.requests[ip] = []
        
        self.requests[ip].append((time.time(), endpoint))

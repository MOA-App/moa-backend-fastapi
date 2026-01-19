from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
import uuid


class RequestIdMiddleware(BaseHTTPMiddleware):
    """
    Middleware que adiciona um ID único a cada requisição.
    Útil para rastreamento e logging.
    """
    
    async def dispatch(self, request: Request, call_next):
        # Gerar ou extrair request ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        
        # Adicionar ao state da request
        request.state.request_id = request_id
        
        # Processar requisição
        response = await call_next(request)
        
        # Adicionar request ID ao header da resposta
        response.headers["X-Request-ID"] = request_id
        
        return response

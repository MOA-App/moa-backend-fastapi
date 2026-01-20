from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from contextlib import asynccontextmanager
import logging

from app.core.config import settings
from app.shared.presentation.middlewares.cors_middleware import setup_cors
from app.shared.presentation.middlewares.request_id_middleware import RequestIdMiddleware
from app.shared.presentation.middlewares.security_headers_middleware import SecurityHeadersMiddleware
from app.modules.auth.presentation.setup import setup_auth_module

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events da aplicação.
    """
    # Startup
    logger.info("🚀 Starting application...")
    logger.info(f"📝 Environment: {settings.ENVIRONMENT}")
    logger.info(
        f"🗄️  Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'Not configured'}")

    # Aqui você pode adicionar:
    # - Criar tabelas no banco (ou usar Alembic)
    # - Inicializar cache (Redis)
    # - Carregar configurações

    yield

    # Shutdown
    logger.info("🛑 Shutting down application...")
    # Aqui você pode adicionar:
    # - Fechar conexões
    # - Limpar recursos


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    description="""
    ## 🔐 API de Autenticação com Clean Architecture

    Sistema completo de autenticação e autorização com:
    - Registro e login de usuários
    - Autenticação JWT
    - Sistema RBAC (Role-Based Access Control)
    - Validação em múltiplas camadas
    - Clean Architecture

    ### 📚 Recursos
    - **Users**: Gerenciamento de usuários
    - **Roles**: Gerenciamento de papéis/funções
    - **Permissions**: Gerenciamento de permissões
    - **Authentication**: Login, registro, tokens JWT

    ### 🔑 Autenticação
    Para acessar endpoints protegidos:
    1. Faça login em `/auth/login`
    2. Copie o `access_token` da resposta
    3. Use o botão "Authorize" (🔓) acima
    4. Digite: `Bearer {seu_token}`
    """,
    version=settings.VERSION,
    lifespan=lifespan,
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    openapi_url="/openapi.json" if settings.DEBUG else None,
)

# ============================================================================
# MIDDLEWARES
# ============================================================================

# CORS
setup_cors(app)

# Request ID
app.add_middleware(RequestIdMiddleware)

# Security Headers
app.add_middleware(SecurityHeadersMiddleware)

# ============================================================================
# MODULES
# ============================================================================

# Setup Auth Module (inclui routers, middlewares e exception handlers)
setup_auth_module(app)


# Aqui você pode adicionar outros módulos:
# setup_products_module(app)
# setup_orders_module(app)

# ============================================================================
# ROOT ENDPOINTS
# ============================================================================

@app.get(
    "/",
    tags=["Root"],
    summary="Root endpoint",
    description="Informações básicas da API"
)
async def root():
    """Endpoint raiz da API"""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "docs": "/docs" if settings.DEBUG else "Disabled in production",
        "health": "/health"
    }


@app.get(
    "/health",
    tags=["Health"],
    summary="Health check",
    description="Verifica se a API está funcionando"
)
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT
    }


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handler para rotas não encontradas"""
    return JSONResponse(
        status_code=404,
        content={
            "error": "not_found",
            "message": f"Rota {request.url.path} não encontrada"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handler para erros internos"""
    logger.error(f"Internal error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "message": "Erro interno do servidor"
        }
    )


# ============================================================================
# STARTUP
# ============================================================================

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )
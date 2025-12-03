'''
from fastapi import APIRouter
from .users.router import router as users_router
from .products.router import router as products_router

api_router = APIRouter()

api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(products_router, prefix="/products", tags=["Products"])
'''

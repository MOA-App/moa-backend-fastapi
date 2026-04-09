from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.shared.infrastructure.database.session import get_db
from ...application.dtos.create_product_dto import CreateProductDTO, UpdateProductDTO
from ...application.dtos.product_response_dto import ProductResponseDTO
from ...application.usecases.create_product_usecase import CreateProductUseCase
from ...application.usecases.list_products_usecase import ListProductsUseCase
from ...application.usecases.get_product_by_id_usecase import GetProductByIdUseCase
from ...application.usecases.get_product_by_sku_usecase import GetProductBySkuUseCase
from ...application.usecases.update_product_usecase import UpdateProductUseCase
from ...application.usecases.delete_product_usecase import DeleteProductUseCase
from ...infrastructure.repositories.product_repository_impl import ProductRepositoryImpl
from ...infrastructure.repositories.category_repository_impl import CategoryRepositoryImpl
from ...domain.exceptions.product_exceptions import (
    ProductNotFoundException,
    ProductAlreadyExistsException
)
from ...domain.exceptions.category_exceptions import CategoryNotFoundException

router = APIRouter(prefix="/products", tags=["Products"])


def get_product_repository(db: AsyncSession = Depends(get_db)) -> ProductRepositoryImpl:
    """Dependency injection para repositório de produtos"""
    return ProductRepositoryImpl(db)


def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepositoryImpl:
    """Dependency injection para repositório de categorias"""
    return CategoryRepositoryImpl(db)


@router.post(
    "/",
    response_model=ProductResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar produto",
    description="Cria um novo produto"
)
async def create_product(
    data: CreateProductDTO,
    product_repository: ProductRepositoryImpl = Depends(get_product_repository),
    category_repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para criar um novo produto"""
    try:
        use_case = CreateProductUseCase(product_repository, category_repository)
        return await use_case.execute(data)
    except ProductAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[ProductResponseDTO],
    summary="Listar produtos",
    description="Lista todos os produtos com filtros opcionais"
)
async def list_products(
    skip: int = Query(0, ge=0, description="Número de registros a pular"),
    limit: int = Query(100, ge=1, le=1000, description="Limite de registros"),
    category_id: Optional[str] = Query(None, description="Filtrar por categoria"),
    active_only: bool = Query(False, description="Apenas produtos ativos"),
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para listar produtos com paginação e filtros"""
    use_case = ListProductsUseCase(repository)
    return await use_case.execute(
        skip=skip,
        limit=limit,
        category_id=category_id,
        active_only=active_only
    )


@router.get(
    "/search",
    response_model=List[ProductResponseDTO],
    summary="Buscar produtos por nome",
    description="Busca produtos por nome (parcial)"
)
async def search_products(
    name: str = Query(..., min_length=1, description="Nome ou parte do nome do produto"),
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para buscar produtos por nome"""
    use_case = ListProductsUseCase(repository)
    return await use_case.search_by_name(name)


@router.get(
    "/search/by-sku",
    response_model=ProductResponseDTO,
    summary="Buscar produto por SKU",
    description="Busca um produto pelo código SKU"
)
async def get_product_by_sku(
    sku: str = Query(..., min_length=1, description="Código SKU do produto"),
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para buscar produto por SKU"""
    try:
        use_case = GetProductBySkuUseCase(repository)
        return await use_case.execute(sku)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{product_id}",
    response_model=ProductResponseDTO,
    summary="Buscar produto por ID",
    description="Busca um produto pelo ID"
)
async def get_product(
    product_id: str,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para buscar produto por ID"""
    try:
        use_case = GetProductByIdUseCase(repository)
        return await use_case.execute(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put(
    "/{product_id}",
    response_model=ProductResponseDTO,
    summary="Atualizar produto",
    description="Atualiza um produto existente"
)
async def update_product(
    product_id: str,
    data: UpdateProductDTO,
    product_repository: ProductRepositoryImpl = Depends(get_product_repository),
    category_repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para atualizar um produto"""
    try:
        use_case = UpdateProductUseCase(product_repository, category_repository)
        return await use_case.execute(product_id, data)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except ProductAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir produto",
    description="Exclui um produto pelo ID"
)
async def delete_product(
    product_id: str,
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para excluir um produto"""
    try:
        use_case = DeleteProductUseCase(repository)
        await use_case.execute(product_id)
    except ProductNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/stats/count",
    response_model=dict,
    summary="Contagem de produtos",
    description="Retorna estatísticas de quantidade de produtos"
)
async def get_product_stats(
    category_id: Optional[str] = Query(None, description="Filtrar por categoria"),
    repository: ProductRepositoryImpl = Depends(get_product_repository)
):
    """Endpoint para obter estatísticas de produtos"""
    use_case = ListProductsUseCase(repository)

    if category_id:
        count = await use_case.count_by_category(category_id)
        return {"category_id": category_id, "count": count}
    else:
        count = await use_case.count()
        return {"total": count}


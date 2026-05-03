from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.shared.infrastructure.database.session import get_db
from ...application.dtos.category_dto import (
    CategoryCreateDTO,
    CategoryResponseDTO
)
from ...application.usecases.create_category_use_case import CreateCategoryUseCase
from ...application.usecases.delete_category_use_case import DeleteCategoryUseCase
from ...application.usecases.list_categories_use_case import ListCategoriesUseCase
from ...application.usecases.get_category_by_id_use_case import GetCategoryByIdUseCase
from ...application.usecases.get_category_by_name_use_case import GetCategoryByNameUseCase
from ...infrastructure.repositories.category_repository_impl import CategoryRepositoryImpl
from ...domain.exceptions.category_exceptions import (
    CategoryAlreadyExistsException,
    CategoryNotFoundException
)

router = APIRouter(prefix="/categories", tags=["Categories"])


def get_category_repository(db: AsyncSession = Depends(get_db)) -> CategoryRepositoryImpl:
    """Dependency injection para repositório de categorias"""
    return CategoryRepositoryImpl(db)


@router.post(
    "/",
    response_model=CategoryResponseDTO,
    status_code=status.HTTP_201_CREATED,
    summary="Criar categoria",
    description="Cria uma nova categoria de produto"
)
async def create_category(
    data: CategoryCreateDTO,
    repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para criar uma nova categoria"""
    try:
        use_case = CreateCategoryUseCase(repository)
        return await use_case.execute(data)
    except CategoryAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.get(
    "/",
    response_model=List[CategoryResponseDTO],
    summary="Listar categorias",
    description="Lista todas as categorias de produtos"
)
async def list_categories(
    repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para listar todas as categorias"""
    use_case = ListCategoriesUseCase(repository)
    return await use_case.execute()


@router.get(
    "/search/by-name",
    response_model=CategoryResponseDTO,
    summary="Buscar categoria por nome",
    description="Busca uma categoria pelo nome"
)
async def get_category_by_name(
    name: str = Query(..., min_length=1, description="Nome da categoria"),
    repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para buscar uma categoria por nome"""
    try:
        use_case = GetCategoryByNameUseCase(repository)
        return await use_case.execute(name)
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get(
    "/{category_id}",
    response_model=CategoryResponseDTO,
    summary="Buscar categoria",
    description="Busca uma categoria pelo ID"
)
async def get_category(
    category_id: str,
    repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para buscar uma categoria por ID"""
    try:
        use_case = GetCategoryByIdUseCase(repository)
        return await use_case.execute(category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.delete(
    "/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Excluir categoria",
    description="Exclui uma categoria pelo ID"
)
async def delete_category(
    category_id: str,
    repository: CategoryRepositoryImpl = Depends(get_category_repository)
):
    """Endpoint para excluir uma categoria"""
    try:
        use_case = DeleteCategoryUseCase(repository)
        await use_case.execute(category_id)
    except CategoryNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )

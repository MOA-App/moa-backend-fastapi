from fastapi import APIRouter, Depends, HTTPException, status
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
    category = await repository.get_by_id(category_id)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoria com ID '{category_id}' não encontrada"
        )
    return CategoryResponseDTO.model_validate(category)


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

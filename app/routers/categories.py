from fastapi import APIRouter, Depends, status

from app.db_depends import get_category_service
from app.schemas import Category as CategorySchema
from app.schemas import CategoryCreate
from app.services.category_service import CategoryService

router = APIRouter(
    prefix='/categories',
    tags=['categories'],
)


@router.get('/', response_model=list[CategorySchema])
async def get_all_categories(
        service: CategoryService = Depends(get_category_service)
) -> list[CategorySchema]:
    """Возвращает список всех активных категорий."""
    return await service.get_all_categories()


@router.post('/', response_model=CategorySchema,
             status_code=status.HTTP_201_CREATED)
async def create_category(
        category: CategoryCreate,
        service: CategoryService = Depends(get_category_service)
) -> CategorySchema:
    """Создает новую категорию товаров."""
    return await service.create_category(category.model_dump())


@router.put('/{category_id}', response_model=CategorySchema)
async def update_category(
        category_id: int,
        category: CategoryCreate,
        service: CategoryService = Depends(get_category_service)
) -> CategorySchema:
    """Обновляет категорию по ее id."""
    return await service.update_category(category_id, category.model_dump())


@router.delete('/{category_id}', status_code=status.HTTP_200_OK)
async def delete_category(
        category_id: int,
        service: CategoryService = Depends(get_category_service)
) -> dict[str, str]:
    """Удаляет категорию по ее id."""
    await service.delete_category(category_id)
    return {'status': 'success', 'message': 'Category marked as inactive'}

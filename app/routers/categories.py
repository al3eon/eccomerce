from fastapi import APIRouter

router = APIRouter(
    prefix='/categories',
    tags=['categories'],
)


@router.get('/')
async def get_all_categories():
    """
    Возвращает список всех категорий товаров.
    """
    return {'message': 'Список всех категорий'}


@router.post('/')
async def create_category():
    """
    Создает новую категорию товаров.
    """
    return {'message': 'Категория создана'}


@router.put('/{category_id}')
async def update_category(category_id: int):
    """
    Обновляет категорию по ее id.
    """
    return {'message': f'Категория с ID {category_id} обновлена'}

@router.delete('/{category_id}')
async def delete_category(category_id: int):
    """
    Удаляет категорию по ее id.
    """
    return {'message': f'Категория с ID {category_id} удалена'}


from fastapi import APIRouter, Depends, status

from app.auth import get_current_seller
from app.db_depends import get_product_service, get_review_service
from app.models import User as UserModel
from app.schemas import Product as ProductSchema
from app.schemas import ProductCreate
from app.schemas import Review as ReviewSchema
from app.services.products_service import ProductsService
from app.services.reviews_service import ReviewsService

router = APIRouter(
    prefix='/products',
    tags=['products'],
)

@router.get('/', response_model=list[ProductSchema])
async def get_all_products(
        service: ProductsService = Depends(get_product_service)
) -> list[ProductSchema]:
    """Возвращает список всех товаров."""
    return await service.get_all_products()


@router.post('/', response_model=ProductSchema,
             status_code=status.HTTP_201_CREATED)
async def create_product(
        product: ProductCreate,
        service: ProductsService = Depends(get_product_service),
        current_user: UserModel = Depends(get_current_seller)
) -> ProductSchema:
    """Создаёт новый товар, привязанный к текущему продавцу."""
    return await service.create_product(product.model_dump(), current_user.id)


@router.get('/category/{category_id}', response_model=list[ProductSchema])
async def get_products_by_category(
        category_id: int,
        service: ProductsService = Depends(get_product_service)
) -> list[ProductSchema]:
    """Возвращает список товаров в указанной категории по её ID."""
    return await service.get_products_by_category(category_id)


@router.get(
    '/{product_id}',
    response_model=ProductSchema,
    status_code=status.HTTP_200_OK
)
async def get_product(
        product_id: int,
        service: ProductsService = Depends(get_product_service)
) -> ProductSchema:
    """Возвращает детальную информацию о товаре по его ID."""
    return await service.get_product_by_id(product_id)


@router.get('/{product_id}/reviews', response_model=list[ReviewSchema])
async def get_review(
        product_id: int,
        service: ReviewsService = Depends(get_review_service)
) -> list[ReviewSchema]:
    """Возвращает детальную информацию об отзыве по его ID."""
    return await service.get_reviews_by_product(product_id)


@router.put('/{product_id}', response_model=ProductSchema)
async def update_product(
        product_id: int,
        product: ProductCreate,
        service: ProductsService = Depends(get_product_service),
        current_user: UserModel = Depends(get_current_seller)
) -> ProductSchema:
    """Обновляет товар, если он принадлежит текущему продавцу."""
    return await service.update_product(product_id, product.model_dump(),
                                        current_user.id)


@router.delete('/{product_id}', response_model=ProductSchema)
async def delete_product(
        product_id: int,
        service: ProductsService = Depends(get_product_service),
        current_user: UserModel = Depends(get_current_seller)
) -> ProductSchema:
    """Выполняет удаление товара, если он принадлежит текущему продавцу."""
    return await service.delete_product(product_id, current_user.id)

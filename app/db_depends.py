from collections.abc import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session_maker
from app.repositories.category_repository import CategoryRepository
from app.repositories.products_repository import ProductsRepository
from app.repositories.reviews_repository import ReviewsRepository
from app.services.category_service import CategoryService
from app.services.products_service import ProductsService
from app.services.reviews_service import ReviewsService


async def get_async_db() -> AsyncGenerator[AsyncSession, None]:
    """Предоставляет асинхронную сессию SQLAlchemy."""
    async with async_session_maker() as session:
        yield session

def get_review_service(
        db: AsyncSession = Depends(get_async_db)
) -> ReviewsService:
    """Создает и возвращает отзыв."""
    review_repository = ReviewsRepository(db)
    product_repository = ProductsRepository(db)
    return ReviewsService(review_repository, product_repository)

def get_product_service(
        db: AsyncSession = Depends(get_async_db)
) -> ProductsService:
    """Создает и возвращает сервис товаров."""
    product_repository = ProductsRepository(db)
    category_repository = CategoryRepository(db)
    return ProductsService(product_repository, category_repository)

def get_category_service(
        db: AsyncSession = Depends(get_async_db)
) -> CategoryService:
    """Создает и возвращает сервис категорий."""
    return CategoryService(CategoryRepository(db))

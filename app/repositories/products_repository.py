from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, Product

from .base import BaseRepository


class ProductsRepository(BaseRepository[Product]):
    """Репозиторий для работы с товарами."""

    def __init__(self, db: AsyncSession) -> None:
        """Инициализирует репозиторий товаров."""
        super().__init__(Product, db)

    async def get_all_active(self) -> list[Product]:
        """Получить все активные товары."""
        result = await self.db.scalars(
            select(Product).join(Category).where(Product.is_active,
                                                 Product.stock > 0,
                                                 Category.is_active)
        )
        return result.all()

    async def get_products_by_category_id(
            self, category_id: int
    ) -> list[Product]:
        """Получить список товаров в указанной категории по ее id."""
        result = await self.db.scalars(
            select(Product).where(Product.category_id == category_id,
                                  Product.is_active)
        )
        return result.all()

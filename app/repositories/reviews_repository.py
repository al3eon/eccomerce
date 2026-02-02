from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.reviews import Review
from app.repositories.base import BaseRepository


class ReviewsRepository(BaseRepository[Review]):
    """Репозиторий для работы с отзывами."""

    def __init__(self, db: AsyncSession) -> None:
        """Инициализация."""
        super().__init__(Review, db)

    async def get_reviews_by_product_id(self, product_id: int) -> list[Review]:
        """Получить список отзывов на товар по его ID."""
        result = await self.db.scalars(
            select(Review).where(Review.product_id == product_id,
                                 Review.is_active)
        )
        return result.all()

    async def get_avg_rating_by_product_id(self, product_id: int) -> Decimal:
        """Вернуть среднее значение рейтинга по указанному товару."""
        result = await self.db.scalar(
            select(func.avg(Review.grade))
            .where(Review.product_id == product_id,
                   Review.is_active)
        )
        return Decimal(str(result)) if result else None

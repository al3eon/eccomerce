from decimal import Decimal

from fastapi import HTTPException, status

from app.repositories.products_repository import ProductsRepository
from app.repositories.reviews_repository import ReviewsRepository
from app.schemas import Review
from app.services.base import BaseService


class ReviewsService(BaseService):
    """Сервис для работы с отзывами."""

    def __init__(self, repository: ReviewsRepository,
                 product_repo: ProductsRepository) -> None:
        """Инициализация."""
        super().__init__(repository)
        self.product_repo = product_repo

    async def get_all_reviews(self) -> list[Review]:
        """Вернуть все отзывы."""
        return await self.get_all()

    async def get_reviews_by_product(self, product_id: int) -> list[Review]:
        """Вернуть отзывы по заданному продукту."""
        await self._validate_product_exists(product_id)
        return await self.repo.get_reviews_by_product_id(product_id)

    async def create_review(self, review: dict, user_id: int) -> Review:
        """Создать новый отзыв, привязанный к текущему пользователю."""
        await self._validate_product_exists(review['product_id'])
        review['user_id'] = user_id
        review_create = await self.create(review)
        await self._update_rating(review['product_id'])
        return review_create

    async def delete_review(
            self, review_id: int, user_id: int, user_role: str
    ) -> None:
        """Мягко удалить отзыв на товар."""
        review = await self.get_or_404(review_id, 'Review not found')
        if review.user_id != user_id and user_role != 'admin':
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You do not have permission to delete this review'
            )
        product_id = review.product_id
        await self.repo.soft_delete(review_id)
        await self._update_rating(product_id)

    async def _validate_product_exists(self, product_id: int) -> None:
        """Проверить существование товара."""
        product = await self.product_repo.get_by_id(product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Product not found'
            )

    async def _update_rating(self, product_id: int) -> None:
        """Пересчитать и обновить рейтинг товара."""
        await self._validate_product_exists(product_id)
        avg_rating = await self.repo.get_avg_rating_by_product_id(product_id)
        await self.product_repo.update(
            product_id,
            {'rating': avg_rating or Decimal('0.0')}
        )

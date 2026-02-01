from sqlalchemy.ext.asyncio import AsyncSession

from app.models.categories import Category

from .base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями."""

    def __init__(self, db: AsyncSession) -> None:
        """Инициализирует репозиторий категорий."""
        super().__init__(Category, db)

from fastapi import HTTPException, status

from app.repositories.category_repository import CategoryRepository
from app.schemas import Category
from app.services.base import BaseService


class CategoryService(BaseService[Category]):
    """Сервис для работы с категориями."""

    def __init__(self, repository: CategoryRepository) -> None:
        """Инициализация."""
        super().__init__(repository)

    async def get_all_categories(self) -> list[Category]:
        """Получить все активные категории."""
        return await self.get_all()

    async def create_category(self, category_data: dict) -> Category:
        """Создать категорию с проверкой родительской."""
        await self._validate_parent_category(category_data.get('parent_id'))
        return await self.create(category_data)

    async def update_category(
            self, category_id: int, category_data: dict
    ) -> Category:
        """Обновить категорию."""
        await self.get_or_404(category_id, 'Category not found')

        if category_data.get('parent_id'):
            await self._validate_parent_category(
                category_data['parent_id'],
                current_id=category_id
            )
        return await self.update_and_return(category_id, category_data)

    async def delete_category(self, category_id: int) -> None:
        """Удалить категорию."""
        await self.get_or_404(category_id, 'Category not found')
        await self.delete(category_id)

    async def _validate_parent_category(self, parent_id: int | None,
                                        current_id: int | None = None) -> None:
        """Проверить что родительская категория существует и валидна."""
        if not parent_id:
            return

        parent = await self.get_or_404(parent_id, 'Parent category not found')

        if current_id and parent.id == current_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail='Category cannot be its own parent'
            )

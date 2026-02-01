from typing import TypeVar

from fastapi import HTTPException, status

from app.repositories.base import BaseRepository

ModelType = TypeVar('ModelType')


class BaseService[ModelType]:
    """Базовый сервис с общей бизнес-логикой."""

    def __init__(self, repository: BaseRepository[ModelType]) -> None:
        """Инициализация."""
        self.repo = repository

    async def get_or_404(self, entity_id: int,
                         detail: str = 'Entity not found') -> ModelType:
        """Получить сущность или выдать 404."""
        entity = await self.repo.get_by_id(entity_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=detail
            )
        return entity

    async def get_all(self) -> list[ModelType]:
        """Получить все активные сущности."""
        return await self.repo.get_all_active()

    async def create(self, data: dict) -> ModelType:
        """Создать новую сущность."""
        return await self.repo.create(data)

    async def update_and_return(self, entity_id: int,
                                data: dict) -> ModelType:
        """Обновить и вернуть сущность."""
        await self.repo.update(entity_id, data)
        return await self.get_or_404(entity_id)

    async def delete(self, entity_id: int) -> None:
        """Удалить сущность с проверкой существования."""
        await self.get_or_404(entity_id)
        await self.repo.soft_delete(entity_id)

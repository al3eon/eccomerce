from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository[ModelType]:
    """Базовый репозиторий для работы с моделями."""

    def __init__(self, model: type[ModelType], db: AsyncSession) -> None:
        """Инициализирует репозиторий."""
        self.model = model
        self.db = db

    async def get_all_active(self) -> list[ModelType]:
        """Получить все активные записи."""
        result = await self.db.scalars(
            select(self.model).where(self.model.is_active)
        )
        return result.all()

    async def get_by_id(self, obj_id: int) -> ModelType:
        """Получить запись по id."""
        return await self.db.scalar(
            select(self.model).where(self.model.id == obj_id,
                                     self.model.is_active)
        )

    async def create(self, data: dict) -> ModelType:
        """Создать запись."""
        instance = self.model(**data)
        self.db.add(instance)
        await self.db.commit()
        await self.db.refresh(instance)
        return instance

    async def update(self, id_data: int, data: dict) -> ModelType:
        """Обновить запись по id."""
        await self.db.execute(
            update(self.model)
            .where(self.model.id == id_data)
            .values(**data)
        )
        await self.db.commit()

    async def soft_delete(self, id_data: int) -> ModelType:
        """Мягко удалить запись по id."""
        await self.update(id_data, {"is_active": False})

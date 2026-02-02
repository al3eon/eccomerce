from decimal import Decimal
from sqlalchemy import select, func, desc
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

    async def get_products_paginate(
            self,
            page: int,
            page_size: int,
            filters: dict | None
    ) -> list[Product]:
        """Получить товары с пагинацией и фильтрами."""

        has_search = filters and filters.get('search_prod')

        if has_search:
            search_value = filters['search_prod'].strip()
            ts_query = func.websearch_to_tsquery('russian', search_value)
            rank_col = func.ts_rank_cd(Product.tsv, ts_query).label('rank')

            stmt = select(Product, rank_col)
            stmt = self._apply_filters(stmt, filters)
            stmt = (
                stmt
                .order_by(desc(rank_col), Product.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await self.db.execute(stmt)
            rows = result.all()
            return [row[0] for row in rows]
        else:
            stmt = select(Product)
            stmt = self._apply_filters(stmt, filters)
            stmt = (
                stmt
                .order_by(Product.id)
                .offset((page - 1) * page_size)
                .limit(page_size)
            )

            result = await self.db.scalars(stmt)
            return result.all()

    async def get_count_products(self, filters: dict | None) -> int:
        """Подсчитать количество товаров с учётом фильтров."""
        stmt = select(func.count()).select_from(Product)
        stmt = self._apply_filters(stmt, filters)
        return await self.db.scalar(stmt) or 0

    def _apply_filters(self, stmt, filters: dict):
        """Применяет фильтры к запросу, включая FTS."""
        stmt = stmt.where(Product.is_active == True)

        if not filters:
            return stmt

        if filters.get('category_id') is not None:
            stmt = stmt.where(Product.category_id == filters['category_id'])

        if filters.get('min_price') is not None:
            stmt = stmt.where(Product.price >= filters['min_price'])

        if filters.get('max_price') is not None:
            stmt = stmt.where(Product.price <= filters['max_price'])

        if filters.get('in_stock') is not None:
            if filters['in_stock']:
                stmt = stmt.where(Product.stock > 0)
            else:
                stmt = stmt.where(Product.stock == 0)

        if filters.get('seller_id') is not None:
            stmt = stmt.where(Product.seller_id == filters['seller_id'])

        if filters.get('search_prod') is not None:
            search_value = filters['search_prod'].strip()
            if search_value:
                ts_query = func.websearch_to_tsquery('russian', search_value)
                stmt = stmt.where(Product.tsv.op('@@')(ts_query))

        return stmt
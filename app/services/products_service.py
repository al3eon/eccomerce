from fastapi import HTTPException, status

from app.models import Product
from app.repositories.category_repository import CategoryRepository
from app.repositories.products_repository import ProductsRepository

from .base import BaseService


class ProductsService(BaseService[Product]):
    """Сервис для работы с товарами."""

    def __init__(self, product_repo: ProductsRepository,
                 category_repo: CategoryRepository) -> None:
        """Инициализация."""
        super().__init__(product_repo)
        self.category_repo = category_repo

    async def get_all_products(self) -> list[Product]:
        """Получить весь список товаров."""
        return await self.get_all()

    async def get_product_by_id(self, product_id: int) -> Product:
        """Получить товар по его id."""
        product = await self.get_or_404(product_id, 'Product not Found')
        await self._validate_category_exists(product.category_id)
        return product

    async def get_products_by_category(
            self, category_id: int
    ) -> list[Product]:
        """Получить товары по id категории."""
        await self._validate_category_exists(category_id)
        return await self.repo.get_products_by_category_id(category_id)

    async def create_product(
            self, product_data: dict, user_id: int
    ) -> Product:
        """Создать товар."""
        await self._validate_category_exists(product_data['category_id'])
        product_data['seller_id'] = user_id
        return await self.create(product_data)

    async def update_product(self, product_id: int, product_data: dict,
                             user_id: int) -> Product:
        """Обновить товар."""
        product = await self.get_or_404(product_id, 'Product not found')
        self._check_ownership(product, user_id)

        if 'category_id' in product_data:
            await self._validate_category_exists(product_data['category_id'])

        return await self.update_and_return(product_id, product_data)

    async def delete_product(self, product_id: int, user_id: int) -> Product:
        """Мягко удалить товар."""
        product = await self.get_or_404(product_id, 'Product not found')
        self._check_ownership(product, user_id)
        await self.repo.soft_delete(product_id)

        return product

    async def _validate_category_exists(self, category_id: int) -> None:
        """Проверить что категория существует и активна."""
        category = await self.category_repo.get_by_id(category_id)
        if not category:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Category not found'
            )

    def _check_ownership(self, product: Product, user_id: int) -> None:
        """Проверить что пользователь владеет товаром."""
        if product.seller_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='You can only modify your own products'
            )

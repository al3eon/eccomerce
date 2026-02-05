from datetime import datetime
from decimal import Decimal
from typing import Annotated
from fastapi import Form

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class CategoryCreate(BaseModel):
    """Модель для создания и обновления категории.

    Используется в POST и PUT запросах.
    """

    name: Annotated[str, Field(
        ..., min_length=3, max_length=50,
        description='Название категории (3-50 символов)'
    )]
    parent_id: Annotated[int | None, Field(
        default=None, description='ID родительской категории, если есть.'
    )]


class Category(CategoryCreate):
    """Модель для ответа с данными категории.

    Используется в GET-запросах.

    """

    id: Annotated[int, Field(
        ..., description='Уникальный идентификатор категории'
    )]
    name: Annotated[str, Field(..., description='Название категории')]
    is_active: Annotated[bool, Field(..., description='Активна ли категория')]


class ProductCreate(BaseModel):
    """Модель для создания и обновления товара.

    Используется в POST и PUT запросах.
    """

    name: Annotated[str, Field(
        ..., min_length=3, max_length=100,
        description='Название товара (3-100 символов)'
    )]
    description: Annotated[str | None, Field(
        None, max_length=200, description='Описание товара (до 500 символов)'
    )]
    price: Annotated[Decimal, Field(
        ..., gt=0, description="Цена товара (больше 0)", decimal_places=2
    )]
    stock: Annotated[int, Field(
        ..., ge=0, description='Количество товара на складе (0 или больше)'
    )]
    category_id: Annotated[int, Field(
        ..., description='ID категории, к которой относится товар'
    )]

    @classmethod
    def as_form(
            cls,
            name: Annotated[str, Form(...)],
            price: Annotated[Decimal, Form(...)],
            stock: Annotated[int, Form(...)],
            category_id: Annotated[int, Form(...)],
            description: Annotated[str | None, Form()] = None,
    ) -> "ProductCreate":
        return cls(
            name=name,
            description=description,
            price=price,
            stock=stock,
            category_id=category_id,
        )


class Product(BaseModel):
    """Модель для ответа с данными товара. Используется в GET-запросах."""

    id: Annotated[int, Field(
        ..., description='Уникальный идентификатор товара'
    )]
    name: Annotated[str, Field(
        ..., min_length=3, max_length=100,
        description='Название товара (3-100 символов)'
    )]
    description: Annotated[str | None, Field(
        None, max_length=200, description='Описание товара (до 500 символов)'
    )]
    price: Annotated[Decimal, Field(
        ..., gt=0, description="Цена товара (больше 0)", decimal_places=2
    )]
    stock: Annotated[int, Field(
        ..., ge=0, description='Количество товара на складе (0 или больше)'
    )]
    category_id: Annotated[int, Field(
        ..., description='ID категории, к которой относится товар'
    )]
    is_active: Annotated[bool, Field(..., description='Активность товара')]
    rating: Annotated[Decimal, Field(..., description='Рейтинг товара')]
    model_config = ConfigDict(from_attributes=True)
    image_url: Annotated[str | None, Field(
        None, description='URL изображения товара'
    )]

class ProductList(BaseModel):
    """
    Список пагинации для товаров.
    """
    items: list[Product] = Field(description='Товары для текущей страницы')
    total: int = Field(ge=0, description='Общее количество товаров')
    page: int = Field(ge=1, description='Номер текущей страницы')
    page_size: int = Field(ge=1,
                           description='Количество элементов на странице')

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    """Модель создания пользователя."""

    email: Annotated[EmailStr, Field(..., description='Email пользователя')]
    password: Annotated[str, Field(
        min_length=8, description='Пароль (минимум 8 символов)'
    )]
    role: Annotated[str, Field(
        default='buyer', pattern='^(buyer|seller)$',
        description='Роль: "buyer" или "seller"'
    )]


class User(BaseModel):
    """Модель пользователя."""

    id: Annotated[int, Field(...)]
    email: Annotated[EmailStr, Field(...)]
    is_active: Annotated[bool, Field(...)]
    role: Annotated[str, Field(...)]

    model_config = ConfigDict(from_attributes=True)


class RefreshTokenRequest(BaseModel):
    """Модель токена для jwt."""

    refresh_token: str


class ReviewCreate(BaseModel):
    """Модель создания отзыва."""

    product_id: Annotated[int, Field(
        ..., description='ID продукта, к которому относится отзыв'
    )]
    comment: Annotated[str | None, Field(None, description='Отзыв к продукту')]
    grade: Annotated[int, Field(..., gt=0, le=5, description='Оценка товара')]


class Review(ReviewCreate):
    """Модель отзыва."""

    id: Annotated[int, Field(
        ..., description='Уникальный идентификатор отзыва'
    )]
    user_id: Annotated[int, Field(
        ...,
        description='Уникальный идентификатор пользователя, оставившего отзыв'
    )]
    comment_date: Annotated[datetime, Field(
        ..., description='Дата и время создания отзыва'
    )]
    is_active: Annotated[bool, Field(..., description='Активен ли отзыв')]

    model_config = ConfigDict(from_attributes=True)


class CartItemBase(BaseModel):
    """Базовая модель для корзины товаров."""
    product_id: Annotated[int, Field(..., description='ID товара')]
    quantity: Annotated[int, Field(..., description='Количество товара')]


class CartItemCreate(CartItemBase):
    """Модель для добавления нового товар в корзину."""


class CartItemUpdate(BaseModel):
    """Модель для обновления количества товара в корзине."""
    quantity: Annotated[int, Field(..., ge=1,
                                   description='Новое количество товара')]


class CartItem(BaseModel):
    """Товар в корзине с данными продукта."""
    id: Annotated[int, Field(..., description='ID позиции корзины')]
    quantity: Annotated[int, Field(..., ge=1, description='Количество товара')]
    product: Annotated[Product, Field(..., description='Информация о товаре')]

    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """Полная информация о корзине пользователя."""
    user_id: Annotated[int, Field(..., description='ID пользователя')]
    items: Annotated[list[CartItem], Field(default_factory=list,
                                           description='Содержимое корзины.')]
    total_quantity: Annotated[int, Field(
        ..., ge=0, description='Общее количество товаров'
    )]
    total_price: Annotated[int, Field(
        ..., ge=0, description='Общая стоимость товаров'
    )]

    model_config = ConfigDict(from_attributes=True)


class OrderItem(BaseModel):
    id: int = Field(..., description='ID позиции заказа')
    product_id: int = Field(..., description='ID товара')
    quantity: int = Field(..., ge=1, description='Количество')
    unit_price: Decimal = Field(
        ..., ge=0,description='Цена за единицу на момент покупки'
    )
    total_price: Decimal = Field(..., ge=0, description='Сумма по позиции')
    product: Product | None = Field(
        None, description='Полная информация о товаре'
    )

    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    id: int = Field(..., description='ID заказа')
    user_id: int = Field(..., description='ID пользователя')
    status: str = Field(..., description='Текущий статус заказа')
    total_amount: Decimal = Field(..., ge=0, description='Общая стоимость')
    created_at: datetime = Field(..., description='Когда заказ был создан')
    updated_at: datetime = Field(
        ..., description='Когда последний раз обновлялся'
    )
    items: list[OrderItem] = Field(
        default_factory=list, description='Список позиций'
    )

    model_config = ConfigDict(from_attributes=True)


class OrderList(BaseModel):
    items: list[Order] = Field(..., description='Заказы на текущей странице')
    total: int = Field(ge=0, description='Общее количество заказов')
    page: int = Field(ge=1, description='Текущая страница')
    page_size: int = Field(ge=1, description='Размер страницы')

    model_config = ConfigDict(from_attributes=True)

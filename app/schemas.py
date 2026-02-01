from decimal import Decimal
from typing import Annotated

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
    image_url: Annotated[str | None, Field(
        None, max_length=200, description='URL изображения товара'
    )]
    stock: Annotated[int, Field(
        ..., ge=0, description='Количество товара на складе (0 или больше)'
    )]
    category_id: Annotated[int, Field(
        ..., description='ID категории, к которой относится товар'
    )]


class Product(ProductCreate):
    """Модель для ответа с данными товара. Используется в GET-запросах."""

    id: Annotated[int, Field(
        ..., description='Уникальный идентификатор товара'
    )]
    is_active: Annotated[bool, Field(..., description='Активность товара')]

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

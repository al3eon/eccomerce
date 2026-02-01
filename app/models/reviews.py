from datetime import datetime

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Review(Base):
    """Модель отзыва."""

    __tablename__ = 'reviews'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    comment: Mapped[str | None] = mapped_column(Text, nullable=True)
    comment_date: Mapped[datetime] = mapped_column(DateTime,
                                                   default=datetime.now)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    grade: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'),
                                            nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'),
                                         nullable=False)

    product: Mapped['Product'] = relationship(
        'Product',
        back_populates='reviews'
    )

    user: Mapped['User'] = relationship(
        'User',
        back_populates='reviews'
    )

    __table_args__ = (
        CheckConstraint('grade >= 1 AND grade <= 5', name='check_grade'),
    )

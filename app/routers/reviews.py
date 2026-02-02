from fastapi import APIRouter, Depends

from app.auth import get_current_buyer, get_current_user
from app.db_depends import get_review_service
from app.models import User as UserModel
from app.schemas import Review as ReviewSchema
from app.schemas import ReviewCreate
from app.services.reviews_service import ReviewsService

router = APIRouter(
    prefix='/reviews',
    tags=['reviews'],
)


@router.get('/', response_model=list[ReviewSchema])
async def get_all_reviews(
        service: ReviewsService = Depends(get_review_service)
) -> list[ReviewSchema]:
    """Возвращает список всех отзывов."""
    return await service.get_all_reviews()


@router.post('/', response_model=ReviewSchema)
async def create_review(
        review: ReviewCreate,
        service: ReviewsService = Depends(get_review_service),
        current_user: UserModel = Depends(get_current_buyer),
) -> ReviewSchema:
    """Создает новый отзыв, привязанный к текущему покупателю."""
    return await service.create_review(review.model_dump(), current_user.id)


@router.delete('/{review_id}', response_model=dict[str, str])
async def delete_review(
        review_id: int,
        service: ReviewsService = Depends(get_review_service),
        current_user: UserModel = Depends(get_current_user)
) -> dict[str, str]:
    """Удаляет отзыв (только владелец или админ)."""
    await service.delete_review(review_id, current_user.id, current_user.role)
    return {'message': 'Review deleted'}

from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseSchema


class DealStatus(str, Enum):
    """Статусы сделки"""

    PENDING = "pending"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DealBase(BaseModel):
    """Базовая схема сделки"""

    seller_id: int
    buyer_id: int
    account_id: int
    status: DealStatus = Field(default=DealStatus.PENDING)


class DealCreate(DealBase):
    """Схема для создания сделки"""

    pass


class DealUpdate(BaseModel):
    """Схема для обновления сделки"""

    status: Optional[DealStatus] = None


class DealInDB(DealBase, BaseSchema):
    """Схема сделки в БД"""

    pass


class Deal(DealInDB):
    """Схема для ответа API"""

    pass


class ReviewBase(BaseModel):
    """Базовая схема отзыва"""

    deal_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    """Схема для создания отзыва"""

    pass


class ReviewUpdate(BaseModel):
    """Схема для обновления отзыва"""

    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class ReviewInDB(ReviewBase, BaseSchema):
    """Схема отзыва в БД"""

    pass


class Review(ReviewInDB):
    """Схема для ответа API"""

    pass

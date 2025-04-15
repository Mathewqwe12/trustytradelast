from typing import Optional, List

from pydantic import BaseModel, Field

from .base import BaseSchema


class AccountBase(BaseModel):
    """Базовая схема игрового аккаунта"""

    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    game: str = Field(..., min_length=1, max_length=100)
    image_url: Optional[str] = None
    seller: Optional[dict] = Field(default_factory=lambda: {"id": 0, "name": "Unknown", "rating": 0})
    is_available: Optional[bool] = True


class AccountCreate(AccountBase):
    """Схема для создания аккаунта"""
    pass


class AccountUpdate(BaseModel):
    """Схема для обновления аккаунта"""

    title: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    game: Optional[str] = Field(None, min_length=1, max_length=100)
    image_url: Optional[str] = None
    seller: Optional[dict] = None
    is_available: Optional[bool] = None


class AccountInDB(AccountBase, BaseSchema):
    """Схема аккаунта в БД"""
    pass


class Account(AccountInDB):
    """Схема для ответа API"""
    pass

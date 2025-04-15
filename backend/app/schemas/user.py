from typing import Optional

from pydantic import BaseModel, Field

from .base import BaseSchema


class UserBase(BaseModel):
    """Базовая схема пользователя"""

    telegram_id: int
    username: Optional[str] = None
    rating: float = Field(default=0.0, ge=0.0, le=5.0)


class UserCreate(UserBase):
    """Схема для создания пользователя"""

    pass


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""

    username: Optional[str] = None
    rating: Optional[float] = Field(default=None, ge=0.0, le=5.0)


class UserInDB(UserBase, BaseSchema):
    """Схема пользователя в БД"""

    pass


class User(UserInDB):
    """Схема для ответа API"""

    pass

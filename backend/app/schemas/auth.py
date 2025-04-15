from typing import Optional

from pydantic import BaseModel


class Token(BaseModel):
    """Схема для токена доступа"""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Схема для данных из токена"""

    telegram_id: Optional[int] = None


class TelegramAuth(BaseModel):
    """Схема для данных авторизации через Telegram"""

    id: int
    first_name: str
    username: str | None = None
    photo_url: str | None = None
    auth_date: int
    hash: str

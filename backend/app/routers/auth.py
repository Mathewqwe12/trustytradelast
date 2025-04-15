from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..auth.telegram import verify_telegram_auth
from ..database.config import get_db
from ..models.user import User
from ..schemas.auth import TelegramAuth

router = APIRouter()


@router.post("/auth/telegram")
async def telegram_auth(
    auth_data: TelegramAuth = Depends(verify_telegram_auth), db: AsyncSession = Depends(get_db)
):
    """
    Авторизация через Telegram

    При успешной авторизации создает или обновляет пользователя в базе
    """
    # Ищем пользователя по telegram_id
    query = select(User).where(User.telegram_id == auth_data.id)
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user:
        # Обновляем существующего пользователя
        user.username = auth_data.username or auth_data.first_name
    else:
        # Создаем нового пользователя
        user = User(
            telegram_id=auth_data.id, username=auth_data.username or auth_data.first_name, rating=0
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)

    return {"user": user, "message": "Successfully authenticated"}

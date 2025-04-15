import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

# Импортируем настройки, которые читают .env
from ..config import settings

# Загружаем переменные окружения (на всякий случай, но settings должны это делать)
load_dotenv()

# Создаем директорию для базы данных если её нет (можно удалить, если SQLite не используется)
# DB_DIR = Path(__file__).parent.parent.parent / "data"
# DB_DIR.mkdir(exist_ok=True)

# Закомментируем хардкодный SQLite URL
# DATABASE_URL = f"sqlite+aiosqlite:///{DB_DIR}/trustytrade.db"

# Используем DATABASE_URL из настроек (settings)
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    # connect_args можно убрать, так как он для SQLite
    # connect_args={"check_same_thread": False}
)

# Создаем фабрику асинхронных сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

async def get_db() -> AsyncSession:
    """Функция-генератор для получения асинхронной сессии БД"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 
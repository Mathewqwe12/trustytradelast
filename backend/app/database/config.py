import os
from pathlib import Path
from typing import AsyncGenerator

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

# Получаем URL базы данных из переменных окружения
DATABASE_URL = os.getenv("DATABASE_URL")

# Если это URL от Railway (начинается с postgres://), преобразуем его в формат asyncpg
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql+asyncpg://", 1)

if not DATABASE_URL:
    DATABASE_URL = "postgresql+asyncpg://trustytrade:trustytrade@localhost:5433/trustytrade_db"

# Создаем асинхронный движок
engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Включаем вывод SQL-запросов в консоль
    pool_size=5,  # Размер пула соединений
    max_overflow=10,  # Максимальное количество дополнительных соединений
)

# Создаем фабрику сессий
AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Получение сессии базы данных"""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close() 
import asyncio
import os
from pathlib import Path

import asyncpg
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Параметры подключения к БД
DB_USER = os.getenv("DB_USER", "trustytrade")
DB_PASSWORD = os.getenv("DB_PASSWORD", "trustytrade")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "trustytrade_db")

async def init_db():
    """Инициализация базы данных"""
    # Подключаемся к БД
    conn = await asyncpg.connect(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        database=DB_NAME
    )

    try:
        # Читаем SQL-скрипт
        sql_path = Path(__file__).parent / "init.sql"
        with open(sql_path, "r", encoding="utf-8") as f:
            sql = f.read()

        # Выполняем SQL-скрипт
        await conn.execute(sql)
        print("База данных успешно инициализирована")

    finally:
        # Закрываем соединение
        await conn.close()

if __name__ == "__main__":
    asyncio.run(init_db()) 
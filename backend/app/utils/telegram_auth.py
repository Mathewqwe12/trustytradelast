import hashlib
import hmac
import json
import os
import time
from typing import Dict

from dotenv import load_dotenv
from fastapi import HTTPException, Request

from ..config import settings

# Загружаем переменные окружения
load_dotenv()

# Получаем токен бота из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not set in environment variables")

# Пути, которые не требуют аутентификации
PUBLIC_PATHS = [
    "/",
    "/docs",
    "/redoc",
    "/openapi.json",
    "/api/v1/health",
    "/api/v1/accounts",
]


def verify_telegram_data(data: Dict) -> bool:
    """
    Проверяет данные авторизации от Telegram

    Args:
        data: Словарь с данными от Telegram Web App

    Returns:
        bool: True если данные верны, иначе False
    """
    if not all(key in data for key in ["hash", "auth_date"]):
        return False

    # Проверяем актуальность данных (не старше 24 часов)
    auth_date = int(data["auth_date"])
    if time.time() - auth_date > 86400:
        return False

    # Получаем хеш от Telegram
    received_hash = data.pop("hash")

    # Создаем строку для проверки
    check_string = "\n".join(f"{k}={v}" for k, v in sorted(data.items()))

    # Создаем secret key из токена бота
    secret = hashlib.sha256(BOT_TOKEN.encode()).digest()

    # Вычисляем хеш
    computed_hash = hmac.new(secret, check_string.encode(), hashlib.sha256).hexdigest()

    return computed_hash == received_hash


async def verify_telegram_auth(request: Request):
    """
    Middleware для проверки Telegram авторизации

    Args:
        request: FastAPI Request объект

    Raises:
        HTTPException: если авторизация не прошла
    """
    # В режиме разработки пропускаем проверку
    if settings.ENV == "development":
        return

    # Извлекаем путь из URL для проверки исключений
    path = request.url.path

    # Проверяем, является ли путь публичным или начинается с публичного пути
    for public_path in PUBLIC_PATHS:
        if path == public_path or path.startswith(f"{public_path}/"):
            return

    # Пропускаем OPTIONS запросы
    if request.method == "OPTIONS":
        return

    # Получаем данные авторизации из заголовка
    auth_data = request.headers.get("X-Telegram-Auth-Data")
    if not auth_data:
        raise HTTPException(status_code=401, detail="No Telegram authentication data provided")

    try:
        # Парсим данные
        data = json.loads(auth_data)

        # Проверяем данные
        if not verify_telegram_data(data):
            raise HTTPException(status_code=401, detail="Invalid Telegram authentication data")

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in authentication data")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication error: {str(e)}")

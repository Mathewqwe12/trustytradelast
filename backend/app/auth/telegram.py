import hashlib
import hmac
import time
from typing import Dict

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from ..config import settings

# Заголовок для Telegram данных
telegram_data_header = APIKeyHeader(name="X-Telegram-Data", auto_error=False)

def verify_telegram_data(data: Dict, bot_token: str) -> bool:
    """
    Проверяет подлинность данных от Telegram
    
    Args:
        data: Словарь с данными от Telegram
        bot_token: Токен бота
    
    Returns:
        bool: True если данные верны, False если нет
    """
    # Получаем хэш из данных
    received_hash = data.pop('hash')
    
    # Сортируем оставшиеся поля
    data_check_string = '\n'.join(
        f"{k}={v}" for k, v in sorted(data.items())
    )
    
    # Создаем secret key из токена бота
    secret_key = hashlib.sha256(bot_token.encode()).digest()
    
    # Вычисляем хэш
    calculated_hash = hmac.new(
        secret_key,
        data_check_string.encode(),
        hashlib.sha256
    ).hexdigest()
    
    # Возвращаем данные обратно
    data['hash'] = received_hash
    
    # Проверяем хэш и время авторизации
    auth_date = data.get('auth_date', 0)
    now = time.time()
    
    # Данные действительны в течение суток
    return calculated_hash == received_hash and now - int(auth_date) < 86400

async def verify_telegram_auth(telegram_data: str = Security(telegram_data_header)) -> Dict:
    """
    Проверяет данные авторизации из заголовка
    
    Args:
        telegram_data: JSON строка с данными авторизации
    
    Returns:
        Dict: Проверенные данные пользователя
    
    Raises:
        HTTPException: Если данные неверны или устарели
    """
    if not telegram_data:
        raise HTTPException(
            status_code=401,
            detail="No Telegram authentication data provided"
        )
    
    try:
        import json
        data = json.loads(telegram_data)
    except:
        raise HTTPException(
            status_code=400,
            detail="Invalid Telegram data format"
        )
    
    if not verify_telegram_data(data, settings.bot_token):
        raise HTTPException(
            status_code=401,
            detail="Invalid Telegram data signature"
        )
    
    return data 
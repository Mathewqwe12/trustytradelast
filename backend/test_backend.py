#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Скрипт для тестирования API бэкенда без запуска полного бота
"""

import json
import logging

import requests
from config import HOST, PORT

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# URL для API
# Используем localhost для подключения и порт 8001
API_BASE_URL = f"http://localhost:8001/api"

def test_get_user_data():
    """Тест получения данных пользователя"""
    try:
        # Тестовый ID пользователя
        user_id = 123456789
        
        # Отправляем GET-запрос
        response = requests.get(f"{API_BASE_URL}/user/{user_id}")
        
        # Выводим результат
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Данные: {response.json() if response.status_code == 200 else 'Нет данных'}")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def test_send_message():
    """Тест отправки сообщения"""
    try:
        # Данные для отправки
        payload = {
            "user_id": 123456789,
            "message": "Тестовое сообщение от локального клиента"
        }
        
        # Отправляем POST-запрос
        response = requests.post(
            f"{API_BASE_URL}/send_message",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Выводим результат
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Данные: {response.json()}")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

def simulate_webhook_data():
    """Симуляция отправки данных через webhook"""
    try:
        # Тестовые данные для webhook
        payload = {
            "update_id": 12345,
            "message": {
                "message_id": 67890,
                "from": {
                    "id": 123456789,
                    "first_name": "Тестовый",
                    "last_name": "Пользователь"
                },
                "text": "Тестовое сообщение от webhook"
            }
        }
        
        # Отправляем POST-запрос
        response = requests.post(
            f"{API_BASE_URL}/webhook",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        # Выводим результат
        logger.info(f"Статус: {response.status_code}")
        logger.info(f"Данные: {response.json()}")
        
    except Exception as e:
        logger.error(f"Ошибка: {e}")

if __name__ == "__main__":
    print("Начало тестирования API бэкенда")
    print("-" * 50)
    
    print("\n1. Тест получения данных пользователя")
    test_get_user_data()
    
    print("\n2. Тест отправки сообщения")
    test_send_message()
    
    print("\n3. Симуляция webhook")
    simulate_webhook_data()
    
    print("\nТестирование завершено") 
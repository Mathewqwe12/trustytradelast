#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import logging
import threading
from typing import Any, Dict, Optional

from config import BOT_TOKEN, SECRET_KEY, WEBAPP_URL
from flask import Flask, jsonify, request
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import CallbackContext, CommandHandler, Filters, MessageHandler, Updater

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


# Инициализация Flask приложения
app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY


class UserDataManager:
    """Менеджер для работы с данными пользователей"""

    def __init__(self):
        self._data: Dict[int, Dict[str, Any]] = {}
        self._lock = threading.Lock()

    def get_user_data(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Получение данных пользователя"""
        with self._lock:
            return self._data.get(user_id)

    def save_user_data(self, user_id: int, data: Dict[str, Any]) -> None:
        """Сохранение данных пользователя"""
        with self._lock:
            self._data[user_id] = data

    def delete_user_data(self, user_id: int) -> None:
        """Удаление данных пользователя"""
        with self._lock:
            self._data.pop(user_id, None)


# Инициализация менеджера данных
user_data_manager = UserDataManager()


def validate_webapp_data(data: Dict[str, Any]) -> bool:
    """Валидация данных от Web App"""
    required_fields = ["action", "timestamp"]
    return all(field in data for field in required_fields)


def start(update: Update, context: CallbackContext) -> None:
    """Обработка команды /start"""
    try:
        user_id = update.effective_user.id
        logger.info(f"Получена команда /start от пользователя {user_id}")
        user = update.effective_user

        keyboard = [
            [InlineKeyboardButton("Открыть мини-приложение", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        message = (
            f"Привет, {user.first_name}! " "Нажмите на кнопку ниже, чтобы открыть мини-приложение."
        )
        update.message.reply_text(message, reply_markup=reply_markup)
        logger.info(f"Ответ на команду /start отправлен пользователю {user.id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /start: {str(e)}")
        update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


def handle_message(update: Update, context: CallbackContext) -> None:
    """Обработка сообщений с данными от Web App"""
    try:
        user_id = update.effective_user.id
        logger.info(f"Получено сообщение от пользователя {user_id}")

        if update.effective_message.web_app_data:
            data = json.loads(update.effective_message.web_app_data.data)

            if not validate_webapp_data(data):
                raise ValueError("Некорректный формат данных")

            user_data_manager.save_user_data(user_id, data)
            logger.info(f"Сохранены данные от пользователя {user_id}: {data}")

            update.message.reply_text("Данные успешно сохранены")
        else:
            update.message.reply_text("Пожалуйста, используйте кнопку для запуска мини-приложения.")
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON от пользователя {user_id}")
        update.message.reply_text("Ошибка формата данных. Пожалуйста, попробуйте снова.")
    except ValueError as e:
        logger.error(f"Ошибка валидации данных: {str(e)}")
        update.message.reply_text("Ошибка валидации данных. Пожалуйста, попробуйте снова.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке сообщения: {str(e)}")
        update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


def error_handler(update: Optional[Update], context: CallbackContext) -> None:
    """Обработчик ошибок"""
    logger.error(f"Update {update} caused error {context.error}", exc_info=context.error)


# API эндпоинты
@app.route("/api/user/<int:user_id>", methods=["GET"])
def get_user_data(user_id: int):
    """Получение данных пользователя по ID"""
    try:
        data = user_data_manager.get_user_data(user_id)
        if data:
            return jsonify({"success": True, "data": data})
        return jsonify({"success": False, "error": "User not found"})
    except Exception as e:
        logger.error(f"Ошибка при получении данных пользователя {user_id}: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route("/api/user/<int:user_id>", methods=["POST"])
def save_user_data(user_id: int):
    """Сохранение данных пользователя"""
    try:
        data = request.json
        if not validate_webapp_data(data):
            return jsonify({"success": False, "error": "Invalid data format"}), 400

        user_data_manager.save_user_data(user_id, data)
        return jsonify({"success": True})
    except Exception as e:
        logger.error(f"Ошибка при сохранении данных пользователя {user_id}: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route("/api/webhook", methods=["POST"])
def telegram_webhook():
    """Обработчик вебхуков от Telegram для Vercel"""
    try:
        if request.method == "POST":
            update = Update.de_json(request.get_json(force=True), None)
            updater = get_updater()
            updater.dispatcher.process_update(update)
            return jsonify({"success": True})
        return jsonify({"success": False})
    except Exception as e:
        logger.error(f"Ошибка при обработке вебхука: {str(e)}")
        return jsonify({"success": False, "error": "Internal server error"}), 500


@app.route("/api/health", methods=["GET"])
def health_check():
    """Проверка работоспособности API"""
    return jsonify({"status": "healthy"})


def get_updater():
    """Получение экземпляра Updater"""
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.web_app_data, handle_message))
    dp.add_error_handler(error_handler)

    return updater


def main():
    """Запуск бота"""
    try:
        updater = get_updater()
        updater.start_polling()
        logger.info("Бот успешно запущен")
        updater.idle()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {str(e)}")
        raise


if __name__ == "__main__":
    main()

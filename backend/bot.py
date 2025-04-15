#!/usr/bin/env python
# -*- coding: utf-8 -*-

import asyncio
import json
import logging
from typing import Any, Dict, Optional

from config import BOT_TOKEN, WEBAPP_URL
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)


def validate_webapp_data(data: Dict[str, Any]) -> bool:
    """Валидация данных от Web App"""
    required_fields = ["action", "timestamp"]
    return all(field in data for field in required_fields)


def get_main_keyboard() -> InlineKeyboardMarkup:
    """Создание основной клавиатуры"""
    keyboard = [
        [InlineKeyboardButton("🎮 Открыть мини-приложение", web_app=WebAppInfo(url=WEBAPP_URL))],
        [InlineKeyboardButton("📝 Мой профиль", callback_data="profile"),
         InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /start"""
    try:
        logger.info("Начинаю обработку команды /start")
        user_id = update.effective_user.id
        logger.info(f"ID пользователя: {user_id}")
        user = update.effective_user
        logger.info(f"Данные пользователя: {user}")

        message = (
            f"👋 Привет, {user.first_name}!\n\n"
            "Я бот для безопасной торговли игровыми аккаунтами. "
            "Используйте мини-приложение для просмотра и создания предложений.\n\n"
            "📌 Основные команды:\n"
            "/help - показать справку\n"
            "/profile - ваш профиль\n"
        )
        logger.info("Подготовил сообщение, пытаюсь отправить")
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
        logger.info(f"Ответ на команду /start отправлен пользователю {user.id}")
    except Exception as e:
        logger.error(f"Детальная ошибка при обработке команды /start: {str(e)}", exc_info=True)
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /help"""
    try:
        user_id = update.effective_user.id
        logger.info(f"Получена команда /help от пользователя {user_id}")

        help_text = (
            "🔍 Справка по использованию бота:\n\n"
            "1️⃣ Для начала работы нажмите кнопку 'Открыть мини-приложение'\n"
            "2️⃣ В приложении вы можете:\n"
            "   • Просматривать доступные аккаунты\n"
            "   • Создавать предложения о продаже\n"
            "   • Участвовать в сделках\n"
            "   • Оставлять отзывы\n\n"
            "📌 Основные команды:\n"
            "/start - перезапустить бота\n"
            "/help - показать эту справку\n"
            "/profile - информация о вашем профиле\n\n"
            "🔐 Безопасность:\n"
            "• Все сделки проходят через гаранта\n"
            "• Используется защищенное соединение\n"
            "• Данные хранятся в зашифрованном виде\n\n"
            "❓ Остались вопросы? Обратитесь в поддержку!"
        )
        await update.message.reply_text(help_text, reply_markup=get_main_keyboard())
        logger.info(f"Ответ на команду /help отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /help: {str(e)}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка команды /profile"""
    try:
        user_id = update.effective_user.id
        user = update.effective_user
        logger.info(f"Получена команда /profile от пользователя {user_id}")

        profile_text = (
            f"👤 Профиль пользователя {user.first_name}\n\n"
            f"🆔 ID: {user_id}\n"
            f"👤 Username: @{user.username or 'не указан'}\n\n"
            "📊 Статистика:\n"
            "💰 Успешных сделок: 0\n"
            "⭐ Рейтинг: 0.0/5.0\n"
            "📝 Отзывов получено: 0\n\n"
            "🔍 Для просмотра подробной статистики и истории сделок\n"
            "используйте мини-приложение 👇"
        )
        await update.message.reply_text(profile_text, reply_markup=get_main_keyboard())
        logger.info(f"Ответ на команду /profile отправлен пользователю {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при обработке команды /profile: {str(e)}")
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка сообщений с данными от Web App"""
    try:
        user_id = update.effective_user.id
        logger.info(f"Получено сообщение от пользователя {user_id}")

        if update.effective_message.web_app_data:
            data = json.loads(update.effective_message.web_app_data.data)

            if not validate_webapp_data(data):
                raise ValueError("Некорректный формат данных")

            # Обработка различных типов действий
            action = data.get("action")
            if action == "create_deal":
                await handle_deal_creation(update, data)
            elif action == "update_profile":
                await handle_profile_update(update, data)
            else:
                await update.message.reply_text("✅ Данные успешно получены")
        else:
            await update.message.reply_text(
                "Пожалуйста, используйте кнопки или мини-приложение для взаимодействия.",
                reply_markup=get_main_keyboard()
            )
    except json.JSONDecodeError:
        logger.error(f"Ошибка декодирования JSON от пользователя {user_id}")
        await update.message.reply_text("❌ Ошибка формата данных. Пожалуйста, попробуйте снова.")
    except ValueError as e:
        logger.error(f"Ошибка валидации данных: {str(e)}")
        await update.message.reply_text("❌ Ошибка валидации данных. Пожалуйста, попробуйте снова.")
    except Exception as e:
        logger.error(f"Неожиданная ошибка при обработке сообщения: {str(e)}")
        await update.message.reply_text("❌ Произошла ошибка. Пожалуйста, попробуйте позже.")


async def handle_deal_creation(update: Update, data: Dict[str, Any]) -> None:
    """Обработка создания сделки"""
    try:
        deal_info = data.get("deal_info", {})
        message = (
            "🎮 Новая сделка создана!\n\n"
            f"🎯 Игра: {deal_info.get('game', 'Не указана')}\n"
            f"💰 Цена: {deal_info.get('price', 0)} RUB\n"
            f"📝 Описание: {deal_info.get('description', 'Нет описания')}\n\n"
            "ℹ️ Используйте мини-приложение для управления сделкой"
        )
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при создании сделки: {str(e)}")
        raise


async def handle_profile_update(update: Update, data: Dict[str, Any]) -> None:
    """Обработка обновления профиля"""
    try:
        profile_info = data.get("profile_info", {})
        message = (
            "✅ Профиль обновлен!\n\n"
            f"👤 Имя: {profile_info.get('name', 'Не указано')}\n"
            f"📱 Контакт: {profile_info.get('contact', 'Не указан')}\n"
            "ℹ️ Изменения вступят в силу в течение нескольких минут"
        )
        await update.message.reply_text(message, reply_markup=get_main_keyboard())
    except Exception as e:
        logger.error(f"Ошибка при обновлении профиля: {str(e)}")
        raise


async def error_handler(update: Optional[Update], context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик ошибок"""
    logger.error("=== ОШИБКА В БОТЕ ===")
    logger.error(f"Update: {update}")
    logger.error(f"Error: {context.error}", exc_info=context.error)
    logger.error(f"Chat data: {context.chat_data}")
    logger.error(f"User data: {context.user_data}")
    logger.error("=== КОНЕЦ ОШИБКИ ===")


def get_application():
    """Получение экземпляра Application"""
    application = Application.builder().token(BOT_TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("profile", profile_command))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_message))
    application.add_error_handler(error_handler)

    return application


def main():
    """Запуск бота"""
    logger.info("Начинаю запуск бота")
    app = get_application()
    logger.info("Application создан, начинаю polling")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Критическая ошибка: {str(e)}")
        raise

import os

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN не найден в .env файле")

# URL веб-приложения
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://trustytradelast.vercel.app/')

# Настройки сервера
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8443))

# Секретный ключ для Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'ваш_секретный_ключ_здесь') 
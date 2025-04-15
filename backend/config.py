import os

from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота
BOT_TOKEN = os.getenv('BOT_TOKEN', '7364226532:AAH8YmUtoB-PmKLI1DcLUTRx2CRPakw7dzw')

# URL веб-приложения - Обновлено для Vercel
WEBAPP_URL = os.getenv('WEBAPP_URL', 'https://tg-app-o1fzwzzon-mathews-projects-6af1e42a.vercel.app')

# Настройки сервера
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', 8443))

# Секретный ключ для Flask
SECRET_KEY = os.getenv('SECRET_KEY', 'ваш_секретный_ключ_здесь') 
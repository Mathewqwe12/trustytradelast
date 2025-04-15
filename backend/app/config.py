import os
from dotenv import load_dotenv # Возвращаем load_dotenv
from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path

# Определяем путь к .env относительно текущего файла
env_path = Path(__file__).parent.parent / '.env' 
load_dotenv(dotenv_path=env_path, override=True) # Загружаем .env из папки backend, перезаписывая системные переменные

# # --- ОТЛАДКА --- 
# print("--- .env DEBUG --- ")
# print(f"DATABASE_URL in env: {os.getenv('DATABASE_URL')}")
# print(f"BOT_TOKEN in env: {os.getenv('BOT_TOKEN')}")
# print(f"SECRET_KEY in env: {os.getenv('SECRET_KEY')}")
# print(f"WEBAPP_URL in env: {os.getenv('WEBAPP_URL')}")
# print("------------------")
# # --- КОНЕЦ ОТЛАДКИ ---

class Settings(BaseSettings):
    # Переменные, которые ДОЛЖНЫ быть прочитаны из .env
    DATABASE_URL: str
    BOT_TOKEN: str
    SECRET_KEY: str
    WEBAPP_URL: str

    # Переменные с значениями по умолчанию
    ENV: str = "development"
    HOST: str = "0.0.0.0"
    PORT: int = 8000 # Используем порт по умолчанию 8000

    # Убираем Config, т.к. load_dotenv загружает переменные в окружение, откуда их читает BaseSettings
    # class Config:
    #     env_file = env_path
    #     extra = "ignore"

settings = Settings()

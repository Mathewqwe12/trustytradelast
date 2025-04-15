import sys
from pathlib import Path
import os

# Добавляем корневую папку проекта в sys.path
# Это позволяет env.py найти пакет 'backend' при запуске alembic из папки backend
project_root = Path(__file__).parent.parent.parent # backend/migrations -> backend -> project_root
sys.path.insert(0, str(project_root))

import asyncio
from logging.config import fileConfig

# Импортируем настройку пути перед другими импортами
# import setup_path  # type: ignore [reportUnusedImport]

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# Импортируем Base из моделей приложения, учитывая пакет backend
from backend.app.models.base import Base
# Импортируем настройки, чтобы получить DATABASE_URL
from backend.app.config import settings

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# --- Используем DATABASE_URL из настроек --- 
# Перезаписываем sqlalchemy.url значением из settings (которое читает .env)
# Это гарантирует, что Alembic использует тот же URL, что и приложение
if settings.DATABASE_URL:
    config.set_main_option('sqlalchemy.url', settings.DATABASE_URL)
else:
    # Можно добавить обработку ошибки, если URL не найден
    raise ValueError("DATABASE_URL not found in settings!")

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    # url = config.get_main_option("sqlalchemy.url") # Используем URL, который мы установили выше
    context.configure(
        url=settings.DATABASE_URL, # Явно передаем URL из настроек
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    configuration = config.get_section(config.config_ini_section)
    configuration["sqlalchemy.url"] = settings.DATABASE_URL
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context."""

    asyncio.run(run_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_async_migrations()

import logging
import traceback

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy import text

from .database.config import engine, get_db
from .database.seed import seed_accounts, seed_users
from .models.base import Base
from .routers import accounts, auth, deals, users
from .utils.telegram_auth import verify_telegram_auth

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", 
    level=logging.DEBUG  # Устанавливаем уровень DEBUG
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TrustyTrade API",
    description="API для сервиса безопасной торговли игровыми аккаунтами",
    version="1.0.0",
)

# Обработчик всех исключений
@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    error_traceback = traceback.format_exc()
    logger.error(f"Unhandled exception: {exc}\nTraceback:\n{error_traceback}")
    return JSONResponse(
        status_code=500,
        content={"error": str(exc), "traceback": error_traceback},
    )

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:4000",
        "http://127.0.0.1:4000",
        "http://localhost:5000",
        "http://127.0.0.1:5000",
        "https://trustytradelast.vercel.app",
        "https://*.up.railway.app"  # Добавляем домен Railway
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware для логирования запросов
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"=== INCOMING REQUEST ===")
    logger.info(f"Method: {request.method}")
    logger.info(f"URL: {request.url}")
    logger.info(f"Path: {request.url.path}")
    logger.info(f"Headers: {dict(request.headers)}")
    
    # Логируем тело запроса для POST/PUT
    if request.method in ["POST", "PUT"]:
        try:
            body = await request.body()
            logger.info(f"Request Body: {body.decode()}")
        except Exception as e:
            logger.error(f"Error reading body: {e}")

    response = await call_next(request)
    
    # Логируем ответ
    logger.info(f"=== RESPONSE ===")
    logger.info(f"Status: {response.status_code}")
    logger.info(f"Headers: {dict(response.headers)}")
    logger.info(f"==================")
    
    return response

# @app.middleware("http")
# async def telegram_auth_middleware(request: Request, call_next):
#     """Middleware для аутентификации Telegram и обработки ошибок"""
#     try:
#         if request.method == "OPTIONS":
#             response = await call_next(request)
#             return response

#         await verify_telegram_auth(request)
#         response = await call_next(request)
#         return response
#     except HTTPException as e:
#         logger.error(f"Ошибка аутентификации: {str(e)}")
#         return JSONResponse(status_code=e.status_code, content={"error": str(e.detail)})
#     except Exception as e:
#         logger.error(f"Неожиданная ошибка в middleware: {str(e)}")
#         return JSONResponse(status_code=500, content={"error": "Внутренняя ошибка сервера"})


# --- Объединенный обработчик Startup ---
@app.on_event("startup")
async def startup_db_and_seed():
    """Инициализация БД и начальное заполнение"""
    logger.info("Запуск инициализации базы данных...")
    try:
        # Получаем сессию и заполняем данными
        async for db in get_db():
            logger.info("Запуск сидинга пользователей...")
            await seed_users(db) # СНАЧАЛА пользователи
            logger.info("Запуск сидинга аккаунтов...")
            await seed_accounts(db) # ПОТОМ аккаунты
            break # Выходим из генератора сессий
        logger.info("Начальное заполнение базы данных завершено.")

    except Exception as e:
        logger.exception(f"Критическая ошибка при инициализации базы данных: {str(e)}")
        raise
    logger.info("Инициализация БД завершена.")


# Подключаем роутеры
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(accounts.router, prefix="/api/v1", tags=["accounts"])
app.include_router(deals.router, prefix="/api/v1", tags=["deals"])


@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {
        "name": "TrustyTrade API",
        "version": "1.0.0",
        "status": "running",
        "docs_url": "/docs",
        "api_url": "/api/v1",
    }

# Добавляем обработчик OPTIONS запросов
@app.options("/{full_path:path}")
async def options_route(request: Request):
    origin = request.headers.get("origin", "")
    if origin in [
        "http://localhost:5175",
        "http://127.0.0.1:5175",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]:
        return JSONResponse(
            status_code=200,
            content={},
            headers={
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "*",
                "Access-Control-Allow-Headers": "*",
                "Access-Control-Allow-Credentials": "true",
            }
        )
    return JSONResponse(content={})

@app.get("/api/v1/test-db")
async def test_db():
    """Тестовый эндпоинт для проверки подключения к базе данных"""
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        logger.error(f"Database connection error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/test-tables")
async def test_tables():
    """Тестовый эндпоинт для проверки таблиц в БД"""
    try:
        async with engine.connect() as conn:
            # Проверяем существование таблицы accounts
            result = await conn.execute(text("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_name = 'accounts'
                )
            """))
            row = result.scalar()  # Используем scalar() вместо fetchone()
            has_accounts = bool(row)  # Преобразуем в bool

            # Если таблица существует, получаем количество записей
            count = 0
            if has_accounts:
                result = await conn.execute(text("SELECT COUNT(*) FROM accounts"))
                count = result.scalar()  # Тоже используем scalar()

            return {
                "status": "ok",
                "has_accounts_table": has_accounts,
                "accounts_count": count
            }
    except Exception as e:
        logger.error(f"Database tables check error: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "message": "Failed to check database tables",
                "error": str(e)
            }
        )

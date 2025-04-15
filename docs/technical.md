# TrustyTrade – Техническая спецификация

## Общее описание системы

TrustyTrade – это Telegram Mini App с ботом для безопасной покупки и продажи игровых аккаунтов. Система включает в себя веб-интерфейс (Mini App), Telegram бот, API-сервер, escrow-сервис, админ-панель и поддержку платежей.

---

## Стек технологий

### Backend
- **Server**: Python (FastAPI)
- **Database**: PostgreSQL
- **Кэширование**: Redis
- **Message Queue**: RabbitMQ (опционально)
- **Payments**: Криптовалюты, Telegram Stars

### Frontend (Telegram Mini App)
- **Framework**: Vanilla JavaScript + Telegram Web App SDK
- **CSS**: Custom CSS с поддержкой Telegram тем
- **Bundler**: Vite.js
- **Hosting**: Vercel/Netlify

### Telegram Integration
- **Bot Framework**: aiogram 3.x
- **Mini App SDK**: telegram-web-app.js
- **Bot API Version**: 6.9+

### DevOps
- **Контейнеризация**: Docker, Docker Compose
- **Логирование и мониторинг**: ELK Stack, Prometheus, Grafana

---

## Архитектура

Проект построен по микросервисной архитектуре:

### Компоненты:
- **Telegram Mini App**: основной пользовательский интерфейс
  - Адаптивный дизайн
  - Поддержка тем Telegram
  - Интеграция с Telegram Web App API
  - Оффлайн поддержка через Service Workers

- **Telegram Bot**: 
  - Точка входа в Mini App
  - Обработка уведомлений
  - Базовые команды
  - Интеграция с платежами

- **REST API**: 
  - Бизнес-логика
  - Авторизация
  - CRUD операции
  - Интеграция с Telegram

- **Escrow-сервис**: безопасные сделки
- **Сервис уведомлений**: push-уведомления
- **Платежный сервис**: криптовалюты и Telegram Stars

---

## API и интеграции

### Внешние API:
- Telegram Bot API
- Telegram Web App SDK
- Blockchain API для криптоплатежей
- Telegram Stars API

### Внутренние API-маршруты:
- `/api/v1/users` — управление пользователями
- `/api/v1/accounts` — управление аккаунтами
- `/api/v1/deals` — управление сделками
- `/api/v1/escrow` — escrow операции
- `/api/v1/payments` — платежные операции
- `/api/v1/notifications` — управление уведомлениями

---

## Mini App UI/UX

### Основные экраны:
1. Главная страница
   - Поиск аккаунтов
   - Категории игр
   - Популярные предложения

2. Страница аккаунта
   - Детальная информация
   - Кнопка покупки
   - Рейтинг продавца

3. Создание объявления
   - Мультистеп форма
   - Загрузка скриншотов
   - Предпросмотр

4. Профиль пользователя
   - Статистика
   - История сделок
   - Настройки

### Особенности:
- Поддержка светлой/темной темы
- Нативные Telegram анимации
- Оффлайн режим
- Быстрая загрузка (< 2s)

---

## Безопасность

- SSL/TLS для API и Mini App
- Защита от CSRF через Telegram авторизацию
- JWT для API запросов
- Rate limiting
- Валидация входных данных
- Escrow для сделок
- 2FA для критических операций

---

## База данных

### Основные таблицы:
- **users** (id, telegram_id, username, rating, created_at)
- **accounts** (id, user_id, game, description, price, status)
- **deals** (id, seller_id, buyer_id, account_id, status)
- **transactions** (id, deal_id, amount, status, hash)
- **reviews** (id, deal_id, rating, comment)

---

## Развертывание

### Frontend (Mini App):
- Vercel/Netlify для хостинга
- Автоматический деплой из main
- Превью для PR

### Backend:
- Docker контейнеры
- CI/CD через GitHub Actions
- Staging и Production среды

---

## Мониторинг

- RUM метрики для Mini App
- API мониторинг через Prometheus
- Логирование через ELK Stack
- Алерты в Telegram

---

## Тестирование

- Unit тесты (Backend: pytest, Frontend: Jest)
- E2E тесты (Cypress)
- Нагрузочное тестирование
- Security аудит

---

## Сопутствующая документация

- User flow и инструкция по работе с ботом
- API-документация (Swagger/OpenAPI)
- Административная документация и сценарии решения конфликтов

---

Это техническая спецификация описывает основные элементы и требования для реализации проекта TrustyTrade.
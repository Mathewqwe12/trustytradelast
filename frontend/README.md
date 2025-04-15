# TrustyTrade Frontend

Веб-приложение для безопасной торговли игровыми аккаунтами через Telegram.

## Разработка

1. Установите зависимости:

```bash
npm install
```

2. Скопируйте файл с переменными окружения:

```bash
cp .env.example .env
```

3. Настройте переменные окружения в `.env`

4. Запустите сервер разработки:

```bash
npm run dev
```

## Деплой на Vercel

1. Установите Vercel CLI:

```bash
npm i -g vercel
```

2. Залогиньтесь в Vercel:

```bash
vercel login
```

3. Настройте переменные окружения в Vercel:

```bash
vercel env add VITE_API_URL
vercel env add VITE_BOT_USERNAME
```

4. Деплой:

```bash
vercel
```

## Структура проекта

```
src/
  ├── api/        # API клиент
  ├── components/ # UI компоненты
  ├── pages/      # Страницы приложения
  ├── services/   # Сервисы (Telegram и др.)
  ├── styles/     # CSS стили
  ├── types/      # TypeScript типы
  └── main.ts     # Точка входа
```

## Технологии

- TypeScript
- Vite
- Telegram Web App SDK

## Установка

1. Установите зависимости:

```bash
npm install
```

2. Запустите сервер разработки:

```bash
npm run dev
```

3. Откройте [http://localhost:5174](http://localhost:5174) в браузере.

## Сборка

Для сборки проекта выполните:

```bash
npm run build
```

Собранные файлы будут находиться в директории `dist`.

## Разработка

- `npm run dev` - запуск сервера разработки
- `npm run build` - сборка проекта
- `npm run preview` - предпросмотр собранного проекта 
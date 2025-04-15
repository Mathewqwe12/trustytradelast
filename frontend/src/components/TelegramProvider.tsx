import { useEffect } from 'react';
import '@twa-dev/sdk';

export default function TelegramProvider({ children }: { children: React.ReactNode }) {
  useEffect(() => {
    // Инициализируем Telegram Web App
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      const app = window.Telegram.WebApp;
      app.ready();
      app.expand(); // Расширяем окно на весь экран
    }
  }, []);

  return <>{children}</>;
} 
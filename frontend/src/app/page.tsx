'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import AccountList from '../components/AccountList';
import dynamic from 'next/dynamic';

const Home = () => {
  const router = useRouter();
  const [webApp, setWebApp] = useState(null);

  useEffect(() => {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      const app = window.Telegram.WebApp;
      app.ready();
      app.setBackgroundColor('#1E1E1E');
      app.setHeaderColor('#1E1E1E');
      setWebApp(app);
    }
  }, []);

  return (
    <main className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-8">
        TrustyTrade
      </h1>
      
      <div className="grid gap-4">
        <button 
          onClick={() => router.push('/deals/new')}
          className="btn-primary"
        >
          Создать предложение
        </button>
        
        <button 
          onClick={() => router.push('/profile')}
          className="btn-secondary"
        >
          Мой профиль
        </button>
      </div>
      
      <h2 className="text-2xl font-bold text-gray-900 dark:text-white mt-8 mb-4">
        Доступные аккаунты
      </h2>
      <AccountList />
    </main>
  );
}

// Отключаем SSR для этого компонента
export default dynamic(() => Promise.resolve(Home), {
  ssr: false
}); 
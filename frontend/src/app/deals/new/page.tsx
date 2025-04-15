'use client';

import { useEffect, useState } from 'react';
import { useForm } from 'react-hook-form';
import dynamic from 'next/dynamic';

type DealForm = {
  title: string;
  description: string;
  price: number;
};

const NewDeal = () => {
  const [webApp, setWebApp] = useState<TelegramWebApp | null>(null);
  const { register, handleSubmit } = useForm<DealForm>();

  useEffect(() => {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      const app = window.Telegram.WebApp;
      app.ready();
      app.MainButton.setText('Создать сделку');
      app.MainButton.show();
      setWebApp(app);
    }
  }, []);

  const onSubmit = (data: DealForm) => {
    if (webApp) {
      webApp.sendData(JSON.stringify(data));
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4 w-full max-w-md">
        <input
          {...register('title')}
          placeholder="Название"
          className="p-2 border rounded"
        />
        <textarea
          {...register('description')}
          placeholder="Описание"
          className="p-2 border rounded"
        />
        <input
          {...register('price', { valueAsNumber: true })}
          type="number"
          placeholder="Цена"
          className="p-2 border rounded"
        />
      </form>
    </main>
  );
}

export default dynamic(() => Promise.resolve(NewDeal), {
  ssr: false
}); 
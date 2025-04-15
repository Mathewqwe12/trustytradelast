'use client';

import { useEffect, useState } from 'react';
import { Account } from '../types/api';
import { convertApiAccount, DisplayAccount } from './AccountCard';

export default function AccountList() {
  const [accounts, setAccounts] = useState<DisplayAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchAccounts();
  }, []);

  async function fetchAccounts() {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/accounts`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data: Account[] = await response.json();
      const displayAccounts = data.map(convertApiAccount);
      setAccounts(displayAccounts);
      setLoading(false);
    } catch (err) {
      console.error('Error fetching accounts:', err);
      setError('Не удалось загрузить аккаунты');
      setLoading(false);
    }
  }

  if (loading) {
    return (
      <div className="flex justify-center items-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-telegram-primary"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center text-red-500 p-4">
        {error}
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {accounts.map((account) => (
        <div
          key={account.id}
          className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300"
        >
          <div className="relative h-48">
            <img
              src={account.imageUrl}
              alt={account.title}
              className="w-full h-full object-cover"
            />
            <div className="absolute top-2 left-2">
              <span className="bg-telegram-primary text-white px-3 py-1 rounded-full text-sm">
                {account.game}
              </span>
            </div>
          </div>
          
          <div className="p-4">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              {account.title}
            </h3>
            
            <div className="flex justify-between items-center">
              <span className="text-2xl font-bold text-telegram-primary">
                {new Intl.NumberFormat('ru-RU').format(account.price)} ₽
              </span>
              
              <div className="flex items-center space-x-1">
                <span className="text-yellow-400">⭐</span>
                <span className="text-gray-600 dark:text-gray-400">
                  {account.seller.rating.toFixed(1)}
                </span>
              </div>
            </div>
            
            <div className="mt-2 text-sm text-gray-500 dark:text-gray-400">
              Продавец: {account.seller.name}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
} 
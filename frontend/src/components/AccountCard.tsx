'use client';

import { useState } from 'react';
import type { Account } from '../types/api';
import { gameImages } from '../styles/images';

export interface DisplayAccount {
  id: number;
  game: string;
  title: string;
  price: number;
  imageUrl: string;
  seller: {
    id: number;
    name: string;
    rating: number;
  };
}

export function convertApiAccount(apiAccount: Account): DisplayAccount {
  const gameImageMap: Record<string, string> = {
    "Dota 2": gameImages.dota2,
    "CS:GO": gameImages.csgo,
    "World of Warcraft": gameImages.wow,
    "Genshin Impact": gameImages.genshin,
    "PUBG": gameImages.pubg,
  };

  const gameImage = gameImageMap[apiAccount.game] || gameImages.placeholder;

  return {
    id: apiAccount.id,
    game: apiAccount.game,
    title: apiAccount.title || apiAccount.description || 'Без названия',
    price: apiAccount.price,
    imageUrl: apiAccount.image_url || gameImage,
    seller: apiAccount.seller,
  };
}

interface AccountCardProps {
  account: DisplayAccount;
  onClick?: (account: DisplayAccount) => void;
}

export default function AccountCard({ account, onClick }: AccountCardProps) {
  const [imageLoaded, setImageLoaded] = useState(false);

  return (
    <div 
      className="card cursor-pointer"
      onClick={() => onClick?.(account)}
    >
      <div className="relative h-48">
        <img
          src={account.imageUrl}
          alt={account.title}
          className={`w-full h-full object-cover transition-opacity duration-300 ${
            imageLoaded ? 'opacity-100' : 'opacity-0'
          }`}
          onLoad={() => setImageLoaded(true)}
          onError={(e) => {
            e.currentTarget.src = gameImages.placeholder;
            setImageLoaded(true);
          }}
        />
        {!imageLoaded && (
          <div className="absolute inset-0 flex items-center justify-center bg-gray-200 dark:bg-gray-700">
            <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-telegram-primary"></div>
          </div>
        )}
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
  );
} 
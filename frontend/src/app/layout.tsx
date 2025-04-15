import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './globals.css';
import dynamic from 'next/dynamic';

const inter = Inter({ subsets: ['latin'] });

const TelegramProvider = dynamic(
  () => import('../components/TelegramProvider'),
  { ssr: false }
);

export const metadata: Metadata = {
  title: 'TrustyTrade',
  description: 'Безопасные сделки в Telegram',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ru">
      <body className={inter.className}>
        <TelegramProvider>
          {children}
        </TelegramProvider>
      </body>
    </html>
  );
} 
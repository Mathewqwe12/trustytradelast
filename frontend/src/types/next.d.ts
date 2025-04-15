/// <reference types="next" />
/// <reference types="next/types/global" />

interface TelegramWebApp {
  ready: () => void;
  backgroundColor: string;
  headerColor: string;
  setBackgroundColor: (color: string) => void;
  setHeaderColor: (color: string) => void;
  sendData: (data: string) => void;
  MainButton: {
    text: string;
    setText: (text: string) => void;
    show: () => void;
    hide: () => void;
  };
}

declare global {
  interface Window {
    Telegram?: {
      WebApp?: TelegramWebApp;
    };
  }
} 
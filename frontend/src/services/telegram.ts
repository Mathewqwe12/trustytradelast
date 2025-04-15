// Определяем тип для Telegram Web App
export interface TelegramWebApp {
  ready: () => void;
  expand: () => void;
  close: () => void;
  MainButton: {
    text: string;
    show: () => void;
    hide: () => void;
    onClick: (callback: () => void) => void;
  };
  BackButton: {
    show: () => void;
    hide: () => void;
    onClick: (callback: () => void) => void;
  };
  onEvent: (eventType: string, callback: () => void) => void;
  offEvent: (eventType: string, callback: () => void) => void;
  sendData: (data: string) => void;
  enableClosingConfirmation: () => void;
  disableClosingConfirmation: () => void;
  HapticFeedback: {
    impactOccurred: (style: 'light' | 'medium' | 'heavy') => void;
    notificationOccurred: (type: 'error' | 'success' | 'warning') => void;
    selectionChanged: () => void;
  };
  backgroundColor: string;
  textColor: string;
  buttonColor: string;
  buttonTextColor: string;
  headerColor: string;
  initData: string;
  initDataUnsafe: {
    query_id: string;
    user: {
      id: number;
      first_name: string;
      last_name?: string;
      username?: string;
      language_code: string;
    };
    auth_date: number;
    hash: string;
  };
  isExpanded: boolean;
  viewportHeight: number;
  viewportStableHeight: number;
  setHeaderColor: (color: string) => void;
  setBackgroundColor: (color: string) => void;
  themeParams: {
    bg_color: string;
  };
}

declare global {
  interface Window {
    Telegram: {
      WebApp: TelegramWebApp;
    };
  }
}

export class TelegramService {
  private static instance: TelegramService;
  private webApp: TelegramWebApp;

  private constructor() {
    if (typeof window !== 'undefined' && window.Telegram?.WebApp) {
      this.webApp = window.Telegram.WebApp;
      this.init();
    } else {
      console.warn('Telegram WebApp не доступен. Используем эмуляцию.');
      this.webApp = this.createFallbackWebApp();
    }
  }

  public static getInstance(): TelegramService {
    if (!TelegramService.instance) {
      TelegramService.instance = new TelegramService();
    }
    return TelegramService.instance;
  }

  private init(): void {
    this.webApp.ready();
    this.webApp.expand();
  }

  private createFallbackWebApp(): TelegramWebApp {
    return {
      ready: () => console.log('WebApp ready called'),
      expand: () => console.log('WebApp expand called'),
      close: () => console.log('WebApp close called'),
      MainButton: {
        text: '',
        show: () => console.log('MainButton show called'),
        hide: () => console.log('MainButton hide called'),
        onClick: (callback) => {
          console.log('MainButton onClick called');
          callback();
        },
      },
      BackButton: {
        show: () => console.log('BackButton show called'),
        hide: () => console.log('BackButton hide called'),
        onClick: (callback) => {
          console.log('BackButton onClick called');
          callback();
        },
      },
      onEvent: (eventType, callback) => {
        console.log('onEvent called', eventType);
        callback();
      },
      offEvent: (eventType, callback) => {
        console.log('offEvent called', eventType);
        callback();
      },
      sendData: (data) => console.log('sendData called', data),
      enableClosingConfirmation: () => console.log('enableClosingConfirmation called'),
      disableClosingConfirmation: () => console.log('disableClosingConfirmation called'),
      HapticFeedback: {
        impactOccurred: (style) => console.log('HapticFeedback impactOccurred called', style),
        notificationOccurred: (type) => console.log('HapticFeedback notificationOccurred called', type),
        selectionChanged: () => console.log('HapticFeedback selectionChanged called'),
      },
      backgroundColor: '#ffffff',
      textColor: '#000000',
      buttonColor: '#2481cc',
      buttonTextColor: '#ffffff',
      headerColor: '#ffffff',
      initData: '',
      initDataUnsafe: {
        query_id: '',
        user: {
          id: 0,
          first_name: 'Test User',
          language_code: 'ru',
        },
        auth_date: 0,
        hash: '',
      },
      isExpanded: false,
      viewportHeight: 0,
      viewportStableHeight: 0,
      setHeaderColor: (color) => console.log('setHeaderColor called', color),
      setBackgroundColor: (color) => console.log('setBackgroundColor called', color),
      themeParams: {
        bg_color: '#ffffff',
      },
    };
  }

  public getWebApp(): TelegramWebApp {
    return this.webApp;
  }

  public hapticImpact(style: 'light' | 'medium' | 'heavy'): void {
    this.webApp?.HapticFeedback?.impactOccurred(style);
  }

  public hapticNotification(type: 'error' | 'success' | 'warning'): void {
    this.webApp?.HapticFeedback?.notificationOccurred(type);
  }

  public hapticSelection(): void {
    this.webApp?.HapticFeedback?.selectionChanged();
  }

  public showBackButton(callback: () => void): void {
    if (!this.webApp) return;
    
    this.webApp.BackButton.show();
    this.webApp.BackButton.onClick(callback);
  }

  public hideBackButton(): void {
    this.webApp?.BackButton?.hide();
  }

  public showMainButton(text: string, callback: () => void): void {
    if (!this.webApp) return;
    
    this.webApp.MainButton.text = text;
    this.webApp.MainButton.onClick(callback);
    this.webApp.MainButton.show();
  }

  public hideMainButton(): void {
    this.webApp?.MainButton?.hide();
  }

  public close(): void {
    this.webApp?.close();
  }
}

// Экспортируем единственный экземпляр сервиса
export const telegram = TelegramService.getInstance(); 
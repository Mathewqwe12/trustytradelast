import { api } from '../api/client';
import { telegram } from '../services/telegram';
import { gameImages } from '../styles/images';
import type { Account } from '../types/api';

export class AccountDetailsPage {
  private container: HTMLElement;
  private account: Account;
  private onBack: () => void;
  private isLoading: boolean = false;
  private loadingIndicator: HTMLElement | null = null;

  constructor(account: Account, onBack: () => void) {
    this.container = document.createElement('div');
    this.container.className = 'account-details-page';
    this.account = account;
    this.onBack = onBack;
    this.render();
  }

  private render(): void {
    // Создаем шапку с кнопкой назад
    const header = document.createElement('header');
    header.className = 'details-header';
    
    // Создаем кнопку назад
    const backButton = document.createElement('button');
    backButton.className = 'back-button';
    backButton.innerHTML = `
      <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
        <path d="M15 18L9 12L15 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
    `;
    backButton.addEventListener('click', () => {
      telegram.hapticImpact('light');
      this.onBack();
    });
    
    // Создаем заголовок
    const title = document.createElement('h1');
    title.textContent = 'Детали аккаунта';
    
    // Добавляем элементы в шапку
    header.appendChild(backButton);
    header.appendChild(title);
    
    // Создаем основной контент
    const content = document.createElement('div');
    content.className = 'details-content';
    
    // Получаем изображение игры
    const gameImage = (gameImages as Record<string, string>)[this.account.game] || gameImages.placeholder;
    
    // Создаем блок с изображением
    const imageContainer = document.createElement('div');
    imageContainer.className = 'account-image';
    
    const img = document.createElement('img');
    img.alt = this.account.game;
    img.src = gameImage;
    img.loading = 'lazy';
    img.addEventListener('load', () => {
      img.classList.add('loaded');
    });
    if (img.complete) {
      img.classList.add('loaded');
    }
    
    imageContainer.appendChild(img);
    content.appendChild(imageContainer);
    
    // Создаем блок с информацией об аккаунте
    const accountInfo = document.createElement('div');
    accountInfo.className = 'account-info';
    
    // Добавляем бейдж игры
    const gameBadge = document.createElement('div');
    gameBadge.className = 'game-badge';
    gameBadge.textContent = this.account.game;
    accountInfo.appendChild(gameBadge);
    
    // Добавляем заголовок аккаунта
    const accountTitle = document.createElement('h2');
    accountTitle.className = 'account-title';
    accountTitle.textContent = this.account.description;
    accountInfo.appendChild(accountTitle);
    
    // Добавляем цену
    const priceTag = document.createElement('div');
    priceTag.className = 'price-tag';
    priceTag.textContent = `${this.formatPrice(this.account.price)} ₽`;
    accountInfo.appendChild(priceTag);
    
    // Добавляем описание аккаунта
    const accountDescription = document.createElement('div');
    accountDescription.className = 'account-description';
    accountDescription.textContent = this.account.description;
    
    // Добавляем дополнительные детали (если есть)
    const accountDetails = document.createElement('div');
    accountDetails.className = 'account-details';
    accountDetails.innerHTML = `
      <h3>Характеристики</h3>
      <ul class="details-list">
        <li>
          <span class="detail-label">Игра:</span>
          <span class="detail-value">${this.account.game}</span>
        </li>
        <li>
          <span class="detail-label">Доступен сразу:</span>
          <span class="detail-value">Да</span>
        </li>
        <li>
          <span class="detail-label">Гарантия:</span>
          <span class="detail-value">7 дней</span>
        </li>
      </ul>
    `;
    
    accountInfo.appendChild(accountDescription);
    accountInfo.appendChild(accountDetails);
    
    // Добавляем информацию о продавце
    const sellerInfo = document.createElement('div');
    sellerInfo.className = 'seller-info';
    sellerInfo.innerHTML = `
      <h3>Продавец</h3>
      <div class="seller-card">
        <div class="seller-name">User ${this.account.user_id}</div>
        <div class="seller-stats">
          <div class="seller-rating">
            <span class="star">⭐</span>
            <span>Новый продавец</span>
          </div>
          <div class="seller-deals">Сделок: --</div>
        </div>
      </div>
    `;
    
    accountInfo.appendChild(sellerInfo);
    
    // Добавляем кнопки действий
    const actionButtons = document.createElement('div');
    actionButtons.className = 'action-buttons';
    
    // Кнопка покупки
    const buyButton = document.createElement('button');
    buyButton.className = 'primary-button buy-button';
    buyButton.textContent = 'Купить сейчас';
    buyButton.addEventListener('click', () => this.handleBuy());
    
    // Кнопка чата
    const chatButton = document.createElement('button');
    chatButton.className = 'secondary-button chat-button';
    chatButton.textContent = 'Написать продавцу';
    chatButton.addEventListener('click', () => this.handleChat());
    
    actionButtons.appendChild(buyButton);
    actionButtons.appendChild(chatButton);
    
    accountInfo.appendChild(actionButtons);
    content.appendChild(accountInfo);
    
    // Добавляем все элементы на страницу
    this.container.appendChild(header);
    this.container.appendChild(content);
    
    // Создаем индикатор загрузки (скрытый изначально)
    this.loadingIndicator = document.createElement('div');
    this.loadingIndicator.className = 'loading-overlay hidden';
    this.loadingIndicator.innerHTML = `
      <div class="spinner"></div>
      <div class="loading-text">Обработка запроса...</div>
    `;
    this.container.appendChild(this.loadingIndicator);
  }

  private formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  private async handleBuy(): Promise<void> {
    if (this.isLoading) return;

    telegram.hapticImpact('medium');
    
    try {
      // Показываем подтверждение
      const tg = window.Telegram?.WebApp;
      if (!tg) {
        throw new Error('Telegram WebApp не доступен');
      }
      
      // Проверяем наличие метода showConfirm
      // @ts-ignore - Игнорируем ошибку проверки типа
      if (typeof tg.showConfirm !== 'function') {
        // Fallback: используем стандартное подтверждение
        const confirmed = confirm(`Вы действительно хотите купить аккаунт "${this.account.description}" за ${this.formatPrice(this.account.price)} ₽?`);
        if (confirmed) {
          await this.processPurchase();
        }
        return;
      }
      
      // Используем нативное подтверждение Telegram
      // @ts-ignore - Игнорируем ошибку проверки типа
      tg.showConfirm(
        `Вы действительно хотите купить аккаунт "${this.account.description}" за ${this.formatPrice(this.account.price)} ₽?`,
        async (confirmed: boolean) => {
          if (confirmed) {
            await this.processPurchase();
          }
        }
      );
    } catch (error) {
      console.error('Ошибка при покупке:', error);
      telegram.hapticNotification('error');
      this.showError('Произошла ошибка. Попробуйте позже.');
    }
  }
  
  private async processPurchase(): Promise<void> {
    this.showLoading(true);
    this.isLoading = true;
    try {
      const response = await api.createDeal({
        account_id: this.account.id
      });

      if (response.status === 'success' && response.data) {
        telegram.hapticNotification('success');
        this.showSuccess('Заявка на покупку создана! Продавец получил уведомление.');
        // TODO: Перейти на страницу сделки
      } else {
        throw new Error(response.error || 'Не удалось создать сделку');
      }
    } catch (error) {
      console.error('Не удалось создать сделку:', error);
      telegram.hapticNotification('error');
      this.showError('Не удалось создать заявку на покупку. Попробуйте позже.');
    } finally {
      this.showLoading(false);
      this.isLoading = false;
    }
  }

  private handleChat(): void {
    telegram.hapticImpact('light');
    try {
      const tg = window.Telegram?.WebApp;
      if (!tg) {
        // Fallback: открываем через обычную ссылку
        window.open(`https://t.me/user${this.account.user_id}`, '_blank');
        return;
      }
      
      // @ts-ignore - Игнорируем ошибку проверки типа
      if (typeof tg.openTelegramLink !== 'function') {
        // Fallback: открываем через обычную ссылку
        window.open(`https://t.me/user${this.account.user_id}`, '_blank');
        return;
      }
      
      // @ts-ignore - Игнорируем ошибку проверки типа
      tg.openTelegramLink(`https://t.me/user${this.account.user_id}`);
    } catch (error) {
      console.error('Ошибка при открытии чата:', error);
      this.showError('Не удалось открыть чат с продавцом');
    }
  }
  
  private showLoading(show: boolean): void {
    if (this.loadingIndicator) {
      if (show) {
        this.loadingIndicator.classList.remove('hidden');
      } else {
        this.loadingIndicator.classList.add('hidden');
      }
    }
  }

  private showError(message: string): void {
    const error = document.createElement('div');
    error.className = 'error-message';
    error.textContent = message;
    this.container.appendChild(error);

    setTimeout(() => {
      error.remove();
    }, 3000);
  }

  private showSuccess(message: string): void {
    const success = document.createElement('div');
    success.className = 'success-message';
    success.textContent = message;
    this.container.appendChild(success);

    setTimeout(() => {
      success.remove();
    }, 3000);
  }

  public mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
  }

  public unmount(): void {
    this.container.remove();
  }
} 
import { api } from '../api/client';
import { telegram } from '../services/telegram';
import { convertApiAccount } from '../components/AccountCard';
import { AccountDetailsPage } from './AccountDetailsPage';
import type { Account } from '../types/api';

export class AccountsListPage {
  private container: HTMLElement;
  private accountsList: HTMLElement;
  private searchInput: HTMLInputElement;
  private accounts: Account[] = [];
  private isLoading: boolean = false;
  private hasMore: boolean = true;
  private currentPage: number = 1;
  private searchTimeout: number | null = null;
  private currentDetailsPage: AccountDetailsPage | null = null;

  constructor() {
    this.container = document.createElement('div');
    this.container.className = 'accounts-list-page';

    // Создаем заголовок
    const header = document.createElement('header');
    header.className = 'header';
    header.innerHTML = `
      <h1>Все аккаунты</h1>
      <div class="search-container">
        <input type="text" placeholder="Поиск по играм или описанию..." class="search-input" />
        <span class="search-icon">🔍</span>
      </div>
    `;

    // Инициализируем поиск
    this.searchInput = header.querySelector('.search-input')!;
    this.searchInput.addEventListener('input', () => this.handleSearch());
    this.searchInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') {
        this.handleSearch();
      }
    });

    // Создаем список аккаунтов
    this.accountsList = document.createElement('div');
    this.accountsList.className = 'accounts-list';

    // Добавляем все элементы на страницу
    this.container.appendChild(header);
    this.container.appendChild(this.accountsList);

    // Инициализируем бесконечную прокрутку
    this.setupInfiniteScroll();

    // Настраиваем кнопку "Назад" в Telegram
    const webApp = telegram.getWebApp();
    webApp.BackButton.show();
    webApp.BackButton.onClick(() => this.handleBack());

    // Загружаем первую страницу
    this.loadAccounts();
  }

  private async loadAccounts(search: string = ''): Promise<void> {
    if (this.isLoading || !this.hasMore) return;

    this.isLoading = true;
    this.showLoader();
    this.clearError();

    try {
      const response = await api.getAccounts({
        page: this.currentPage,
        search: search
      });

      if (response.status === 'success' && response.data) {
        if (!Array.isArray(response.data)) {
          throw new Error('Некорректный формат данных от API');
        }
        
        const accounts = response.data;
        
        if (this.currentPage === 1) {
          this.accounts = [];
          this.accountsList.innerHTML = '';
        }

        this.accounts = [...this.accounts, ...accounts];
        
        const EXPECTED_PAGE_SIZE = 100;
        this.hasMore = accounts.length >= EXPECTED_PAGE_SIZE;
        
        if (accounts.length > 0) {
          this.currentPage++;
        } else {
          this.hasMore = false;
        }

        this.updateAccountsList();
      } else {
        throw new Error(response.error || 'Не удалось загрузить аккаунты');
      }
    } catch (error) {
      console.error('Failed to load accounts:', error);
      
      const errorMessage = error instanceof Error && error.message.includes('NetworkError') 
        ? 'Ошибка подключения к серверу. Проверьте интернет-соединение.'
        : 'Не удалось загрузить аккаунты. Попробуйте обновить страницу.';
        
      this.showError(errorMessage, true);
      this.hasMore = false;
    } finally {
      this.isLoading = false;
      this.hideLoader();
    }
  }

  private handleSearch(): void {
    if (this.searchTimeout) {
      window.clearTimeout(this.searchTimeout);
    }

    this.showLoader();

    this.searchTimeout = window.setTimeout(() => {
      this.currentPage = 1;
      this.hasMore = true;
      this.accounts = [];
      this.updateAccountsList();
      this.loadAccounts(this.searchInput.value.trim());
    }, 300);
  }

  private setupInfiniteScroll(): void {
    const sentinel = document.createElement('div');
    sentinel.className = 'scroll-sentinel';
    this.container.appendChild(sentinel);

    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadAccounts(this.searchInput.value.trim());
        }
      });
    });

    observer.observe(sentinel);
  }

  private updateAccountsList(): void {
    this.accountsList.innerHTML = '';

    if (!this.accounts || this.accounts.length === 0) {
      const emptyState = document.createElement('div');
      emptyState.className = 'empty-state';
      emptyState.innerHTML = `
        <div class="empty-icon">🔍</div>
        <h2>Ничего не найдено</h2>
        <p>Попробуйте изменить параметры поиска</p>
      `;
      this.accountsList.appendChild(emptyState);
      return;
    }

    this.accounts.forEach(account => {
      try {
        const displayAccount = convertApiAccount(account);
        
        const card = document.createElement('div');
        card.className = 'account-card';
        card.addEventListener('click', () => this.handleAccountClick(account));
        
        const imageContainer = document.createElement('div');
        imageContainer.className = 'card-image';
        
        const img = document.createElement('img');
        img.src = displayAccount.imageUrl;
        img.alt = displayAccount.title;
        img.loading = 'lazy';
        
        img.addEventListener('load', () => {
          img.classList.add('loaded');
        });
        
        if (img.complete) {
          img.classList.add('loaded');
        }
        
        imageContainer.appendChild(img);
        card.appendChild(imageContainer);
        
        const contentContainer = document.createElement('div');
        contentContainer.className = 'card-content';
        
        const gameBadge = document.createElement('div');
        gameBadge.className = 'game-badge';
        gameBadge.textContent = displayAccount.game;
        contentContainer.appendChild(gameBadge);
        
        const title = document.createElement('h3');
        title.className = 'card-title';
        title.textContent = displayAccount.title;
        contentContainer.appendChild(title);
        
        const footer = document.createElement('div');
        footer.className = 'card-footer';
        
        const price = document.createElement('div');
        price.className = 'price';
        price.textContent = `${this.formatPrice(displayAccount.price)} ₽`;
        footer.appendChild(price);
        
        const seller = document.createElement('div');
        seller.className = 'seller';
        
        const sellerName = document.createElement('span');
        sellerName.className = 'seller-name';
        sellerName.textContent = displayAccount.seller.name;
        seller.appendChild(sellerName);
        
        const sellerRating = document.createElement('span');
        sellerRating.className = 'seller-rating';
        
        const star = document.createElement('span');
        star.className = 'star';
        star.textContent = '⭐';
        
        sellerRating.appendChild(star);
        sellerRating.appendChild(document.createTextNode(displayAccount.seller.rating.toFixed(1)));
        seller.appendChild(sellerRating);
        
        footer.appendChild(seller);
        contentContainer.appendChild(footer);
        card.appendChild(contentContainer);
        
        this.accountsList.appendChild(card);
      } catch (error) {
        console.error('Error rendering account card:', error);
      }
    });
  }

  private formatPrice(price: number): string {
    return new Intl.NumberFormat('ru-RU').format(price);
  }

  private handleAccountClick(account: Account): void {
    this.currentDetailsPage = new AccountDetailsPage(account);
    this.currentDetailsPage.mount(document.body);
    this.container.style.display = 'none';
  }

  private handleBack(): void {
    if (this.currentDetailsPage) {
      this.currentDetailsPage.unmount();
      this.currentDetailsPage = null;
      this.container.style.display = 'block';
    } else {
      window.history.back();
    }
  }

  private showLoader(): void {
    const loader = document.createElement('div');
    loader.className = 'loader';
    loader.innerHTML = '<div class="spinner"></div>';
    this.container.appendChild(loader);
  }

  private hideLoader(): void {
    const loader = this.container.querySelector('.loader');
    if (loader) {
      loader.remove();
    }
  }

  private clearError(): void {
    const error = this.container.querySelector('.error-message');
    if (error) {
      error.remove();
    }
  }

  private showError(message: string, withRetry: boolean = false): void {
    this.clearError();
    
    const errorContainer = document.createElement('div');
    errorContainer.className = 'error-message';
    
    const errorText = document.createElement('p');
    errorText.textContent = message;
    errorContainer.appendChild(errorText);
    
    if (withRetry) {
      const retryButton = document.createElement('button');
      retryButton.className = 'retry-button';
      retryButton.textContent = 'Попробовать снова';
      retryButton.onclick = () => {
        this.clearError();
        this.currentPage = 1;
        this.hasMore = true;
        this.loadAccounts(this.searchInput.value.trim());
      };
      errorContainer.appendChild(retryButton);
    }
    
    this.container.appendChild(errorContainer);
  }

  public mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
  }

  public unmount(): void {
    this.container.remove();
  }
} 
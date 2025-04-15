import { api } from '../api/client';
import { telegram } from '../services/telegram';
import { convertApiAccount } from '../components/AccountCard';
import { AccountDetailsPage } from './AccountDetailsPage';
import type { Account } from '../types/api';

export class HomePage {
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
    this.container.className = 'home-page';

    // Создаем заголовок
    const header = document.createElement('header');
    header.className = 'header';
    header.innerHTML = `
      <h1>Аккаунты</h1>
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

    // Загружаем первую страницу
    this.loadAccounts();
  }

  private async loadAccounts(search: string = ''): Promise<void> {
    if (this.isLoading || !this.hasMore) return;

    this.isLoading = true;
    this.showLoader();
    this.clearError(); // Очищаем предыдущие ошибки

    try {
      const response = await api.getAccounts({
        page: this.currentPage,
        search: search
      });

      if (response.status === 'success' && response.data) {
        // Проверяем, что данные - это массив
        if (!Array.isArray(response.data)) {
          throw new Error('Некорректный формат данных от API');
        }
        
        const accounts = response.data;
        
        // Если это первая страница, очищаем список
        if (this.currentPage === 1) {
          this.accounts = [];
          this.accountsList.innerHTML = '';
        }

        // Добавляем новые аккаунты
        this.accounts = [...this.accounts, ...accounts];
        
        // Проверяем, есть ли еще аккаунты (предполагаем, что сервер возвращает max 100 записей)
        const EXPECTED_PAGE_SIZE = 100;
        this.hasMore = accounts.length >= EXPECTED_PAGE_SIZE;
        
        // Увеличиваем номер страницы только если получили данные
        if (accounts.length > 0) {
          this.currentPage++;
        } else {
          this.hasMore = false; // Если нет данных, то и пагинации нет
        }

        this.updateAccountsList();
      } else {
        throw new Error(response.error || 'Не удалось загрузить аккаунты');
      }
    } catch (error) {
      console.error('Failed to load accounts:', error);
      
      // Определяем, является ли ошибка сетевой или нет
      const errorMessage = error instanceof Error && error.message.includes('NetworkError') 
        ? 'Ошибка подключения к серверу. Проверьте интернет-соединение.'
        : 'Не удалось загрузить аккаунты. Попробуйте обновить страницу.';
        
      this.showError(errorMessage, true); // Добавляем кнопку обновления
      this.hasMore = false; // Останавливаем дальнейшую загрузку при ошибке
    } finally {
      this.isLoading = false;
      this.hideLoader();
    }
  }

  private handleSearch(): void {
    const query = this.searchInput.value.trim();
    
    // Отменяем предыдущий таймаут
    if (this.searchTimeout) {
      window.clearTimeout(this.searchTimeout);
    }

    // Показываем индикатор загрузки
    this.showLoader();

    // Устанавливаем новый таймаут
    this.searchTimeout = window.setTimeout(() => {
      this.currentPage = 1;
      this.hasMore = true;
      this.accounts = [];
      this.updateAccountsList();
      this.loadAccounts(query);
    }, 300);
  }

  private setupInfiniteScroll(): void {
    // Создаем сентинел для бесконечной прокрутки
    const sentinel = document.createElement('div');
    sentinel.className = 'scroll-sentinel';
    this.container.appendChild(sentinel);

    // Создаем наблюдатель
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          this.loadAccounts(this.searchInput.value.trim());
        }
      });
    });

    // Начинаем наблюдение
    observer.observe(sentinel);
  }

  private updateAccountsList(): void {
    // Очищаем список
    this.accountsList.innerHTML = '';

    // Проверяем наличие аккаунтов
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

    // Создаем простой HTML для карточек вместо использования компонента AccountCard
    this.accounts.forEach(account => {
      try {
        const displayAccount = convertApiAccount(account);
        
        // Создаем элемент карточки
        const card = document.createElement('div');
        card.className = 'account-card';
        
        // Создаем контейнер для изображения
        const imageContainer = document.createElement('div');
        imageContainer.className = 'card-image';
        
        // Создаем изображение
        const img = document.createElement('img');
        img.src = displayAccount.imageUrl;
        img.alt = displayAccount.title;
        img.loading = 'lazy';
        
        // Добавляем обработчик загрузки изображения
        img.addEventListener('load', () => {
          img.classList.add('loaded');
        });
        
        // Если изображение уже загружено
        if (img.complete) {
          img.classList.add('loaded');
        }
        
        // Добавляем изображение в контейнер
        imageContainer.appendChild(img);
        card.appendChild(imageContainer);
        
        // Создаем контейнер для контента
        const contentContainer = document.createElement('div');
        contentContainer.className = 'card-content';
        
        // Добавляем бейдж игры
        const gameBadge = document.createElement('div');
        gameBadge.className = 'game-badge';
        gameBadge.textContent = displayAccount.game;
        contentContainer.appendChild(gameBadge);
        
        // Добавляем заголовок
        const title = document.createElement('h3');
        title.className = 'card-title';
        title.textContent = displayAccount.title;
        contentContainer.appendChild(title);
        
        // Создаем футер карточки
        const footer = document.createElement('div');
        footer.className = 'card-footer';
        
        // Добавляем цену
        const price = document.createElement('div');
        price.className = 'price';
        price.textContent = `${this.formatPrice(displayAccount.price)} ₽`;
        footer.appendChild(price);
        
        // Создаем блок с информацией о продавце
        const seller = document.createElement('div');
        seller.className = 'seller';
        
        // Имя продавца
        const sellerName = document.createElement('span');
        sellerName.className = 'seller-name';
        sellerName.textContent = displayAccount.seller.name;
        seller.appendChild(sellerName);
        
        // Рейтинг продавца
        const sellerRating = document.createElement('span');
        sellerRating.className = 'seller-rating';
        
        const star = document.createElement('span');
        star.className = 'star';
        star.textContent = '⭐';
        sellerRating.appendChild(star);
        
        const ratingText = document.createTextNode(
          ` ${displayAccount.seller.rating.toFixed(1)}`
        );
        sellerRating.appendChild(ratingText);
        
        seller.appendChild(sellerRating);
        footer.appendChild(seller);
        
        // Добавляем футер в контент
        contentContainer.appendChild(footer);
        
        // Добавляем контент в карточку
        card.appendChild(contentContainer);
        
        // Добавляем обработчик клика
        card.addEventListener('click', () => this.handleAccountClick(account));
        
        // Добавляем карточку в список
        this.accountsList.appendChild(card);
        
      } catch (error) {
        console.error('Error rendering account:', error, account);
      }
    });
  }

  private formatPrice(price: number): string {
    return price.toLocaleString('ru-RU');
  }

  private handleAccountClick(account: Account): void {
    telegram.hapticImpact('light');
    
    // Создаем страницу деталей
    this.currentDetailsPage = new AccountDetailsPage(account, () => {
      this.currentDetailsPage?.unmount();
      this.currentDetailsPage = null;
      this.container.style.display = 'block';
    });

    // Скрываем главную страницу
    this.container.style.display = 'none';

    // Показываем страницу деталей
    this.currentDetailsPage.mount(document.body);
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
    const existingError = this.container.querySelector('.error-message');
    if (existingError) {
      existingError.remove();
    }
  }

  private showError(message: string, withRetry: boolean = false): void {
    this.clearError();
    const error = document.createElement('div');
    error.className = 'error-message';
    
    const messageEl = document.createElement('p');
    messageEl.textContent = message;
    error.appendChild(messageEl);
    
    if (withRetry) {
      const retryButton = document.createElement('button');
      retryButton.className = 'retry-button';
      retryButton.textContent = 'Обновить';
      retryButton.addEventListener('click', () => {
        this.currentPage = 1;
        this.hasMore = true;
        this.loadAccounts(this.searchInput.value.trim());
      });
      error.appendChild(retryButton);
    }
    
    this.container.insertBefore(error, this.accountsList);
  }

  public mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
  }

  public unmount(): void {
    this.container.remove();
  }
} 
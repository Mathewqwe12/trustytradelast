import type {
  Account,
  ApiResponse,
  CreateAccountRequest,
  CreateReviewRequest,
  Deal,
  Review,
  UpdateAccountRequest,
  User
} from '../types/api';

// Интерфейс для параметров запроса аккаунтов
interface GetAccountsParams {
  page?: number;
  search?: string;
}

// Интерфейс для создания сделки
interface CreateDealParams {
  account_id: number;
}

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;
  private readonly API_DEFAULT_URL = 'http://localhost:8000/api/v1';

  constructor() {
    // В production будем использовать реальный URL бэкенда
    this.baseUrl = import.meta.env.PROD 
      ? 'https://api.trustytrade.app/api/v1'
      : this.API_DEFAULT_URL;
  }

  // Утилиты для работы с API
  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<{ status: 'success' | 'error'; data?: T; error?: string }> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        method: 'GET',
        ...options,
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json',
          ...(this.token ? { 'Authorization': `Bearer ${this.token}` } : {}),
          ...options.headers,
        },
      });

      if (!response.ok) {
        if (response.status === 401) {
          return {
            status: 'error',
            error: 'Необходима авторизация'
          };
        }
        
        if (response.status === 404) {
          return {
            status: 'error',
            error: 'Ресурс не найден'
          };
        }
        
        if (response.status >= 500) {
          return {
            status: 'error',
            error: 'Ошибка сервера. Попробуйте позже.'
          };
        }
        
        try {
          // Пытаемся прочитать детали ошибки из ответа
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Неизвестная ошибка');
        } catch (e) {
          // Если не можем прочитать JSON, используем статус ответа
          throw new Error(`Ошибка ${response.status}: ${response.statusText}`);
        }
      }

      const data = await response.json();
      return {
        status: 'success',
        data,
      };
    } catch (error) {
      console.error('API Error:', error);
      
      // Пробрасываем NetworkError дальше для обработки на уровне компонентов
      if (error instanceof TypeError && error.message.includes('Network')) {
        return {
          status: 'error',
          error: `NetworkError: ${error.message}`
        };
      }
      
      return {
        status: 'error',
        error: error instanceof Error ? error.message : 'Неизвестная ошибка',
      };
    }
  }

  // Аутентификация
  public setToken(token: string): void {
    this.token = token;
  }

  public clearToken(): void {
    this.token = null;
  }

  // Методы для работы с пользователями
  public async getCurrentUser(): Promise<ApiResponse<User>> {
    return this.request<User>('/users/me');
  }

  public async getUserById(id: number): Promise<ApiResponse<User>> {
    return this.request<User>(`/users/${id}`);
  }

  // Методы для работы с аккаунтами
  public async getAccounts(params: GetAccountsParams = {}) {
    const searchParams = new URLSearchParams();
    if (params.page) {
      // Преобразуем page в skip (page начинается с 1)
      const skip = (params.page - 1) * 100; // 100 - это limit по умолчанию
      searchParams.append('skip', skip.toString());
    }
    if (params.search) {
      searchParams.append('search', params.search);
    }
    // Всегда добавляем limit
    searchParams.append('limit', '100');

    return this.request<Account[]>(`/accounts?${searchParams.toString()}`);
  }

  public async getAccount(id: number) {
    return this.request<Account>(`/accounts/${id}`);
  }

  public async createAccount(data: CreateAccountRequest): Promise<ApiResponse<Account>> {
    return this.request<Account>('/accounts', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  public async updateAccount(id: number, data: UpdateAccountRequest): Promise<ApiResponse<Account>> {
    return this.request<Account>(`/accounts/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(data),
    });
  }

  public async deleteAccount(id: number): Promise<ApiResponse<void>> {
    return this.request<void>(`/accounts/${id}`, {
      method: 'DELETE',
    });
  }

  // Методы для работы со сделками
  public async createDeal(params: CreateDealParams) {
    return this.request<Deal>('/deals', {
      method: 'POST',
      body: JSON.stringify(params),
    });
  }

  public async getDeals() {
    return this.request<Deal[]>('/deals');
  }

  public async getDeal(id: number) {
    return this.request<Deal>(`/deals/${id}`);
  }

  public async confirmDeal(id: number) {
    return this.request<Deal>(`/deals/${id}/confirm`, {
      method: 'POST',
    });
  }

  public async cancelDeal(id: number) {
    return this.request<Deal>(`/deals/${id}/cancel`, {
      method: 'POST',
    });
  }

  // Методы для работы с отзывами
  public async createReview(data: CreateReviewRequest): Promise<ApiResponse<Review>> {
    return this.request<Review>('/reviews', {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  public async getUserReviews(userId: number): Promise<ApiResponse<Review[]>> {
    return this.request<Review[]>(`/users/${userId}/reviews`);
  }
}

// Экспортируем единственный экземпляр клиента
export const api = new ApiClient(); 
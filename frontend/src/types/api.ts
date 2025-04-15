// Базовые типы данных
export interface User {
  id: number;
  name: string;
  username?: string;
  rating: number;
  deals_completed: number;
  reviews_count: number;
  created_at: string;
  updated_at: string;
}

export interface Account {
  id: number;
  game: string;
  title: string;
  description?: string;
  price: number;
  image_url?: string;
  is_available: boolean;
  created_at: string;
  updated_at: string;
  seller: {
    id: number;
    name: string;
    rating: number;
  };
}

export interface Deal {
  id: number;
  account_id: number;
  buyer_id: number;
  seller_id: number;
  status: 'pending' | 'in_progress' | 'completed' | 'cancelled';
  price: number;
  created_at: string;
  updated_at: string;
}

export interface Review {
  id: number;
  deal_id: number;
  rating: number;
  comment: string;
  created_at: string;
}

// API ответы
export interface ApiResponse<T> {
  status: 'success' | 'error';
  data?: T;
  error?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
  pages: number;
}

// API запросы
export interface CreateAccountRequest {
  game: string;
  title: string;
  description: string | null;
  price: number;
  image_url?: string | null;
  seller?: {
    id: number;
    name: string;
    rating: number;
  } | null;
  is_available?: boolean | null;
}

export interface UpdateAccountRequest extends Partial<CreateAccountRequest> {}

export interface CreateDealRequest {
  account_id: number;
}

export interface CreateReviewRequest {
  deal_id: number;
  rating: number;
  comment: string;
}

// Параметры запросов
export interface AccountsQueryParams {
  page?: number;
  size?: number;
  game?: string;
  min_price?: number;
  max_price?: number;
  search?: string;
  sort_by?: 'price' | 'created_at' | 'rating';
  sort_order?: 'asc' | 'desc';
} 
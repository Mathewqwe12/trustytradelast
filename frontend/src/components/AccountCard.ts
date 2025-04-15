import type { Account as ApiAccount } from "../types/api";
import { gameImages } from "../styles/images";

// Интерфейс для отображения карточки аккаунта
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

// Функция для преобразования API аккаунта в отображаемый формат
export function convertApiAccount(apiAccount: ApiAccount): DisplayAccount {
  // Создаем маппинг игр к изображениям
  const gameImageMap: Record<string, string> = {
    "Dota 2": gameImages.dota2,
    "CS:GO": gameImages.csgo,
    "World of Warcraft": gameImages.wow,
    "Genshin Impact": gameImages.genshin,
    "PUBG": gameImages.pubg,
  };

  // Получаем изображение из маппинга или используем плейсхолдер
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

export class AccountCard {
  private container: HTMLElement;
  private account: DisplayAccount;
  private onClick?: (account: DisplayAccount) => void;

  constructor(
    account: DisplayAccount,
    onClick?: (account: DisplayAccount) => void
  ) {
    this.container = document.createElement("div");
    this.container.className = "account-card";
    this.container.setAttribute("data-game", account.game);
    this.account = account;
    this.onClick = onClick;
    
    this.render();
  }

  private render(): void {
    // Очищаем контейнер
    this.container.innerHTML = "";
    
    // Создаем блок для изображения
    const imageContainer = document.createElement("div");
    imageContainer.className = "card-image";
    
    // Создаем изображение
    const img = document.createElement("img");
    img.alt = this.account.title;
    img.src = this.account.imageUrl;
    img.loading = "lazy";
    
    // Обработчик загрузки изображения
    img.onload = () => {
      img.classList.add("loaded");
    };
    
    img.onerror = () => {
      // Устанавливаем плейсхолдер при ошибке загрузки
      img.src = gameImages.placeholder || '';
      img.classList.add("loaded");
    };
    
    // Если изображение уже загружено из кэша
    if (img.complete) {
      img.classList.add("loaded");
    }
    
    imageContainer.appendChild(img);
    this.container.appendChild(imageContainer);
    
    // Создаем контент карточки
    const contentContainer = document.createElement("div");
    contentContainer.className = "card-content";
    
    // Бейдж игры
    const gameBadge = document.createElement("div");
    gameBadge.className = "game-badge";
    gameBadge.textContent = this.account.game;
    contentContainer.appendChild(gameBadge);
    
    // Заголовок
    const title = document.createElement("h3");
    title.className = "card-title";
    title.textContent = this.account.title;
    contentContainer.appendChild(title);
    
    // Футер карточки
    const footer = document.createElement("div");
    footer.className = "card-footer";
    
    // Цена
    const price = document.createElement("div");
    price.className = "price";
    price.textContent = `${this.formatPrice(this.account.price)} ₽`;
    footer.appendChild(price);
    
    // Блок с информацией о продавце
    const seller = document.createElement("div");
    seller.className = "seller";
    
    // Имя продавца
    const sellerName = document.createElement("span");
    sellerName.className = "seller-name";
    sellerName.textContent = this.account.seller.name;
    seller.appendChild(sellerName);
    
    // Рейтинг продавца
    const sellerRating = document.createElement("span");
    sellerRating.className = "seller-rating";
    
    const star = document.createElement("span");
    star.className = "star";
    star.textContent = "⭐";
    sellerRating.appendChild(star);
    
    const ratingText = document.createTextNode(
      ` ${this.account.seller.rating.toFixed(1)}`
    );
    sellerRating.appendChild(ratingText);
    
    seller.appendChild(sellerRating);
    footer.appendChild(seller);
    
    // Добавляем футер в контент
    contentContainer.appendChild(footer);
    
    // Добавляем контент в карточку
    this.container.appendChild(contentContainer);

    // Добавляем обработчик клика
    if (this.onClick) {
      this.container.addEventListener("click", () =>
        this.onClick?.(this.account)
      );
    }
  }

  private formatPrice(price: number): string {
    return price.toLocaleString("ru-RU");
  }

  public mount(parent: HTMLElement): void {
    parent.appendChild(this.container);
  }

  public unmount(): void {
    this.container.remove();
  }
}

import "./styles/main.css";
import { api } from './api/client';
import { HomePage } from "./pages/HomePage";
import { gameImages } from "./styles/images";

// Предзагрузка изображений для улучшения UX
function preloadImages() {
  // Предзагружаем все изображения игр
  Object.values(gameImages).forEach(imageUrl => {
    const img = new Image();
    img.src = imageUrl;
  });
}

// Добавляем простой индикатор загрузки
function showInitialLoader() {
  const loader = document.createElement('div');
  loader.className = 'initial-loader';
  loader.innerHTML = `
    <div class="spinner"></div>
    <div class="loading-text">Загрузка приложения...</div>
  `;
  document.body.appendChild(loader);
  return loader;
}

// Инициализируем приложение
const app = document.getElementById("app");
if (!app) {
  throw new Error("Root element not found");
}

// Показываем индикатор загрузки
const loader = showInitialLoader();

// Предзагружаем изображения перед монтированием страницы
preloadImages();

try {
  // Создаем и монтируем главную страницу
  const homePage = new HomePage();
  homePage.mount(app);
  
  // Удаляем индикатор загрузки после монтирования
  setTimeout(() => {
    loader.remove();
  }, 300); // Небольшая задержка для более плавного UX
} catch (error) {
  console.error('Ошибка при инициализации приложения:', error);
  
  // Показываем сообщение об ошибке вместо индикатора загрузки
  loader.innerHTML = `
    <div class="error-icon">⚠️</div>
    <div class="error-text">Ошибка при загрузке приложения</div>
    <button class="retry-button">Повторить</button>
  `;
  
  // Добавляем обработчик для кнопки повтора
  const retryButton = loader.querySelector('.retry-button');
  if (retryButton) {
    retryButton.addEventListener('click', () => {
      window.location.reload();
    });
  }
}

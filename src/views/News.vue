<template>
  <div class="news-container">
    <div class="news-header">
      <h1 class="news-title">Новости спортивного программирования</h1>
      <p class="news-subtitle">Будьте в курсе последних событий и турниров</p>
    </div>

    <div class="news-controls">
      <div class="search-container">
        <input
          v-model="searchQuery"
          type="text"
          placeholder="Поиск по новостям..."
          class="search-input"
          @input="filterNews"
        />
        <svg class="search-icon" viewBox="0 0 24 24">
          <path
            fill="currentColor"
            d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
          />
        </svg>
      </div>
      <div class="sort-controls">
        <button
          @click="sortByDate('asc')"
          :class="{ active: sortOrder === 'asc' }"
          class="sort-button"
        >
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path
              fill="currentColor"
              d="M19 17h3l-4 4-4-4h3V3h2v14zm-7 2h2v-8h-2v8zM9 3H7v14h2V3zM5 3H3v14h2V3z"
            />
          </svg>
          Сначала новые
        </button>
        <button
          @click="sortByDate('desc')"
          :class="{ active: sortOrder === 'desc' }"
          class="sort-button"
        >
          <svg viewBox="0 0 24 24" width="16" height="16">
            <path
              fill="currentColor"
              d="M19 7h3l-4-4-4 4h3v14h2V7zm-7 2h2v8h-2V9zM9 17H7V3h2v14zm-4 0H3V3h2v14z"
            />
          </svg>
          Сначала старые
        </button>
      </div>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <Loader />
    </div>

    <div v-else-if="error" class="error-message">
      <svg viewBox="0 0 24 24" width="24" height="24">
        <path
          fill="currentColor"
          d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"
        />
      </svg>
      <p>{{ error }}</p>
      <button @click="fetchNews" class="retry-button">Попробовать снова</button>
    </div>

    <div v-else class="news-grid">
      <TransitionGroup name="news-item">
        <article
          v-for="item in filteredNews"
          :key="item.id"
          class="news-card"
          @click="openNews(item)"
        >
          <div class="news-card-content">
            <div class="news-date">{{ formatDate(item.date) }}</div>
            <h3 class="news-card-title">{{ item.title }}</h3>
            <p class="news-card-excerpt">
              {{ truncateContent(item.content, 120) }}
            </p>
          </div>
          <div class="news-card-footer">
            <button class="read-more">Читать далее →</button>
          </div>
        </article>
      </TransitionGroup>
    </div>

    <div v-if="selectedNews" class="news-modal" @click.self="closeModal">
      <div class="modal-content">
        <button class="close-modal" @click="closeModal">
          <svg viewBox="0 0 24 24" width="24" height="24">
            <path
              fill="currentColor"
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </button>
        <div class="modal-header">
          <span class="modal-date">{{ formatDate(selectedNews.date) }}</span>
          <h2 class="modal-title">{{ selectedNews.title }}</h2>
        </div>
        <div class="modal-body">
          <p>{{ selectedNews.content }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";

// Создаем экземпляр axios с базовым URL
const api = axios.create({
  baseURL: "http://10.8.0.23:8000",
  timeout: 5000,
});

const newsData = ref({
  count: 0,
  results: [],
});

const searchQuery = ref("");
const isLoading = ref(true);
const error = ref(null);
const sortOrder = ref("asc");
const selectedNews = ref(null);

const fetchNews = async () => {
  try {
    isLoading.value = true;
    error.value = null;

    const response = await api.get("/news/");
    newsData.value = response.data;
  } catch (err) {
    console.error("Ошибка при загрузке новостей:", err);
    error.value = `Не удалось загрузить новости. ${
      err.response?.status === 404
        ? "Сервер не найден"
        : "Пожалуйста, попробуйте позже"
    }`;
  } finally {
    isLoading.value = false;
  }
};

const filteredNews = computed(() => {
  let result = [...newsData.value.results];

  // Фильтрация по поиску
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    result = result.filter(
      (item) =>
        item.title.toLowerCase().includes(query) ||
        item.content.toLowerCase().includes(query)
    );
  }

  // Сортировка по дате
  result.sort((a, b) => {
    const dateA = parseDate(a.date);
    const dateB = parseDate(b.date);
    return sortOrder.value === "asc" ? dateB - dateA : dateA - dateB;
  });

  return result;
});

const parseDate = (dateString) => {
  const [day, month, year] = dateString.split(".").map(Number);
  return new Date(year, month - 1, day).getTime();
};

const formatDate = (dateString) => {
  const [day, month, year] = dateString.split(".");
  const months = [
    "января",
    "февраля",
    "марта",
    "апреля",
    "мая",
    "июня",
    "июля",
    "августа",
    "сентября",
    "октября",
    "ноября",
    "декабря",
  ];
  return `${day} ${months[parseInt(month) - 1]} ${year}`;
};

const truncateContent = (text, maxLength) => {
  return text.length > maxLength ? text.substring(0, maxLength) + "..." : text;
};

const sortByDate = (order) => {
  sortOrder.value = order;
};

const openNews = (newsItem) => {
  selectedNews.value = newsItem;
  document.body.style.overflow = "hidden";
};

const closeModal = () => {
  selectedNews.value = null;
  document.body.style.overflow = "auto";
};

onMounted(() => {
  fetchNews();
});
</script>

<style scoped>
.news-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}

.news-header {
  text-align: center;
  margin-bottom: 2.5rem;
}

.news-title {
  font-size: 2.5rem;
  font-weight: 800;
  margin-bottom: 0.5rem;
  background: #ef4444;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.news-subtitle {
  font-size: 1.1rem;
  color: #64748b;
}

.news-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.search-container {
  position: relative;
  flex-grow: 1;
  max-width: 400px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem 0.75rem 2.5rem;
  border: 2px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 1rem;
  transition: all 0.3s ease;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
}

.search-input:focus {
  outline: none;
  border-color: #2563eb;
}

.search-icon {
  position: absolute;
  left: 1rem;
  top: 50%;
  transform: translateY(-50%);
  width: 1.25rem;
  height: 1.25rem;
  color: #94a3b8;
}

.sort-controls {
  display: flex;
  gap: 0.5rem;
}

.sort-button {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.5rem 1rem;
  background: white;
  border: 1px solid #e2e8f0;
  border-radius: 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.sort-button:hover {
  background: #f8fafc;
  border-color: #c7d2fe;
}

.sort-button.active {
  background: #2563eb;
  color: white;
  border-color: #2563eb;
}

.loading-spinner {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 400px;
  gap: 1rem;
}
.error-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  gap: 1rem;
  text-align: center;
  color: #ef4444;
}

.error-message svg {
  color: #ef4444;
}

.retry-button {
  margin-top: 1rem;
  padding: 0.5rem 1.5rem;
  background: #8b5cf6;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-button:hover {
  background: #7c3aed;
}

.news-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.news-card {
  background: white;
  border-radius: 0.75rem;
  overflow: hidden;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 1px solid #e2e8f0;
  cursor: pointer;
}

.news-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
  border-color: #8b5cf6;
}

.news-card-content {
  padding: 1.5rem;
  flex-grow: 1;
}

.news-date {
  font-size: 0.75rem;
  color: #2563eb;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.news-card-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 0.75rem;
  color: #1e293b;
  line-height: 1.3;
}

.news-card-excerpt {
  color: #475569;
  font-size: 0.9375rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.news-card-footer {
  padding: 0 1.5rem 1.5rem;
}

.read-more {
  background: none;
  border: none;
  color: #ef4444;
  font-weight: 600;
  cursor: pointer;
  padding: 0;
  font-size: 0.875rem;
  display: flex;
  align-items: center;
  gap: 0.25rem;
  transition: color 0.2s;
}

.read-more:hover {
  color: #7c3aed;
}

.news-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: white;
  border-radius: 0.75rem;
  max-width: 800px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-modal {
  position: absolute;
  top: 1rem;
  right: 1rem;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 50%;
  transition: background 0.2s;
  z-index: 10;
}

.close-modal:hover {
  background: #f1f5f9;
}

.modal-header {
  padding: 2rem 2rem 1rem;
  border-bottom: 1px solid #e2e8f0;
  position: sticky;
  top: 0;
  background: white;
  z-index: 5;
}

.modal-date {
  font-size: 0.875rem;
  color: #8b5cf6;
  font-weight: 600;
  display: block;
  margin-bottom: 0.5rem;
}

.modal-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0;
  color: #1e293b;
}

.modal-body {
  padding: 1.5rem 2rem 2rem;
  line-height: 1.7;
  color: #334155;
}

/* Анимации */
.news-item-enter-active,
.news-item-leave-active {
  transition: all 0.5s ease;
}
.news-item-enter-from,
.news-item-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

@media (max-width: 768px) {
  .news-title {
    font-size: 2rem;
  }

  .news-controls {
    flex-direction: column;
    align-items: stretch;
  }

  .search-container {
    max-width: 100%;
  }

  .sort-controls {
    justify-content: flex-end;
  }
}

@media (max-width: 480px) {
  .news-title {
    font-size: 1.75rem;
  }

  .modal-header {
    padding: 1.5rem 1.5rem 1rem;
  }

  .modal-body {
    padding: 1rem 1.5rem 1.5rem;
    font-size: 0.9375rem;
    line-height: 1.6;
    color: #334155;
  }
}
</style>

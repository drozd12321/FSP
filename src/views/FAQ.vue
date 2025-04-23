<template>
  <div class="faq-container">
    <h1 class="faq-title">Часто задаваемые вопросы</h1>
    <p class="faq-subtitle">Мы собрали ответы на самые популярные вопросы</p>

    <div class="search-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск по вопросам..."
        class="search-input"
        @input="filterQuestions"
      />
      <svg class="search-icon" viewBox="0 0 24 24">
        <path
          fill="currentColor"
          d="M15.5 14h-.79l-.28-.27a6.5 6.5 0 0 0 1.48-5.34c-.47-2.78-2.79-5-5.59-5.34a6.505 6.505 0 0 0-7.27 7.27c.34 2.8 2.56 5.12 5.34 5.59a6.5 6.5 0 0 0 5.34-1.48l.27.28v.79l4.25 4.25c.41.41 1.08.41 1.49 0 .41-.41.41-1.08 0-1.49L15.5 14zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
        />
      </svg>
    </div>

    <div v-if="isLoading" class="loading-spinner">
      <Loader />
    </div>

    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="fetchFaqData" class="retry-button">
        Попробовать снова
      </button>
    </div>

    <div v-else>
      <div class="faq-stats">
        Найдено вопросов: {{ filteredQuestions.length }} из {{ faqData.count }}
      </div>
      <div class="faq-list">
        <TransitionGroup name="faq-item">
          <div
            v-for="item in filteredQuestions"
            :key="item.id"
            class="faq-item"
            :class="{ 'is-active': activeQuestion === item.id }"
            @click="toggleQuestion(item.id)"
          >
            <div class="faq-question">
              <h3 class="question-text">{{ item.question }}</h3>
              <svg
                class="arrow-icon"
                viewBox="0 0 24 24"
                :class="{ 'rotate-180': activeQuestion === item.id }"
              >
                <path
                  fill="currentColor"
                  d="M7.41 8.59L12 13.17l4.59-4.58L18 10l-6 6-6-6 1.41-1.41z"
                />
              </svg>
            </div>
            <Transition name="slide-fade">
              <div v-if="activeQuestion === item.id" class="faq-answer">
                <p>{{ item.answer }}</p>
              </div>
            </Transition>
          </div>
        </TransitionGroup>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import Loader from "@/components/Loader.vue";

const api = axios.create({
  baseURL: "http://10.8.0.23:8000",
  timeout: 5000,
});

const faqData = ref({
  count: 0,
  results: [],
});

const activeQuestion = ref(null);
const searchQuery = ref("");
const filteredQuestions = ref([]);
const isLoading = ref(true);
const error = ref(null);

const fetchFaqData = async () => {
  try {
    isLoading.value = true;
    error.value = null;

    const response = await api.get("/faq/");
    faqData.value = response.data;
    filteredQuestions.value = [...faqData.value.results];
  } catch (err) {
    console.error("Ошибка при загрузке FAQ:", err);
    error.value = `Не удалось загрузить вопросы. ${
      err.response?.status === 404
        ? "Сервер не найден"
        : "Пожалуйста, попробуйте позже"
    }`;
  } finally {
    isLoading.value = false;
  }
};

const toggleQuestion = (id) => {
  activeQuestion.value = activeQuestion.value === id ? null : id;
};

const filterQuestions = () => {
  if (!searchQuery.value) {
    filteredQuestions.value = [...faqData.value.results];
    return;
  }

  const query = searchQuery.value.toLowerCase();
  filteredQuestions.value = faqData.value.results.filter(
    (item) =>
      item.question.toLowerCase().includes(query) ||
      item.answer.toLowerCase().includes(query)
  );
};

onMounted(() => {
  fetchFaqData();
});
</script>

<style scoped>
.faq-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}

.faq-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: #1a1a1a;
  margin-bottom: 0.5rem;
  text-align: center;
  background: #ef4444;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.faq-subtitle {
  font-size: 1.1rem;
  color: #64748b;
  text-align: center;
  margin-bottom: 2rem;
}

.search-container {
  position: relative;
  margin-bottom: 2rem;
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
  border-color: #8b5cf6;
  box-shadow: 0 0 0 3px rgba(139, 92, 246, 0.2);
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

.faq-stats {
  font-size: 0.875rem;
  color: #64748b;
  margin-bottom: 1rem;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.faq-item {
  border-radius: 0.5rem;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: all 0.3s ease;
  border: 1px solid #e2e8f0;
  cursor: pointer;
}

.faq-item:hover {
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transform: translateY(-3px);
  border-color: #c7d2fe;
}

.faq-item.is-active {
  border: 2px solid #2563eb;
}

.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem;
}

.question-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: #1e293b;
  margin: 0;
  flex: 1;
}

.arrow-icon {
  width: 1.5rem;
  height: 1.5rem;
  color: #64748b;
  transition: transform 0.3s ease;
}

.arrow-icon.rotate-180 {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.25rem 1.25rem;
  color: #475569;
  line-height: 1.6;
}

.loading-spinner {
  display: flex;
  justify-content: center;

  height: 400px;
}

.spinner {
  animation: rotate 2s linear infinite;
  width: 50px;
  height: 50px;
}

.spinner .path {
  stroke: #8b5cf6;
  stroke-linecap: round;
  animation: dash 1.5s ease-in-out infinite;
}

.error-message {
  color: #ef4444;
  text-align: center;
  padding: 1rem;
  background: #fee2e2;
  border-radius: 0.5rem;
  margin: 1rem 0;
}

.retry-button {
  margin-top: 0.5rem;
  padding: 0.5rem 1rem;
  background: #8b5cf6;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  transition: background 0.2s;
}

.retry-button:hover {
  background: #7c3aed;
}

@keyframes rotate {
  100% {
    transform: rotate(360deg);
  }
}

@keyframes dash {
  0% {
    stroke-dasharray: 1, 150;
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -35;
  }
  100% {
    stroke-dasharray: 90, 150;
    stroke-dashoffset: -124;
  }
}

/* Анимации */
.faq-item-enter-active,
.faq-item-leave-active {
  transition: all 0.5s ease;
}
.faq-item-enter-from,
.faq-item-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}
.slide-fade-leave-active {
  transition: all 0.2s cubic-bezier(1, 0.5, 0.8, 1);
}
.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

@media (max-width: 640px) {
  .faq-title {
    font-size: 2rem;
  }

  .faq-question {
    padding: 1rem;
  }
}
</style>

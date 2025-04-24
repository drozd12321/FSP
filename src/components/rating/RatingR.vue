<template>
  <div class="rating-container">
    <h2 class="rating-title">Рейтинг пользователей</h2>
    <div class="rating-controls">
      <input type="text" placeholder="Поиск по имени" class="search-input" />
      <select class="filter-select">
        <option>Все категории</option>
        <option>Лидеры</option>
        <option>Новички</option>
      </select>
    </div>
    <div v-if="dataLoad" class="loader-overlay"><Loader /></div>
    <div v-else>
      <div class="table-grid">
        <div class="grid-header">
          <div class="grid-cell rank-header">#</div>
          <div class="grid-cell user-header">Пользователь</div>
          <div class="grid-cell points-header">Очки</div>
        </div>
        <div class="grid-body">
          <div
            class="grid-row"
            v-for="(user, index) in displayedUsers"
            :key="user.id"
          >
            <div class="grid-cell rank-cell">
              {{ (currentPage - 1) * itemsPerPage + index + 1 }}
            </div>
            <div class="grid-cell user-cell">
              <div class="user-info">
                <img :src="user.avatar" class="user-avatar" alt="Аватар" />
                <span>{{ user.name }}</span>
              </div>
            </div>
            <div class="grid-cell points-cell">{{ user.rating }}</div>
          </div>
        </div>
      </div>
      <div class="pagination">
        <button
          class="pagination-btn prev-btn"
          @click="prevPage"
          :disabled="isFirstPage()"
        >
          ←
        </button>
        <button
          v-for="page in pages"
          :key="page.number"
          class="pagination-btn"
          :class="{ active: currentPage === page.number }"
          @click="goToPage(page.number)"
        >
          {{ page.number }}
        </button>
        <button
          class="pagination-btn next-btn"
          @click="nextPage"
          :disabled="isLastPage()"
        >
          →
        </button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { usePagination } from "@/use/usePagination";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import Loader from "../Loader.vue";

const users = ref([]);
const itemsPerPage = 10;
const totalPages = Math.ceil(users.length / itemsPerPage);
console.log(totalPages);
const {
  currentPage,
  goToPage,
  isFirstPage,
  isLastPage,
  nextPage,
  pages,
  prevPage,
} = usePagination(1, totalPages);

const displayedUsers = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage;
  const end = start + itemsPerPage;
  return users.value.slice(start, end);
});
const getRatingClass = (rating) => {
  if (rating >= 9) return "high-rating";
  if (rating >= 8) return "medium-rating";
  return "low-rating";
};
const dataLoad = ref();
const getUsers = async () => {
  try {
    dataLoad.value = true;
    const response = await axios.get("http://10.8.0.23:8000/users/");
    users.value = response.data;
    console.log(users.value);
    dataLoad.value = false;
    return response.data;
  } catch (error) {
    dataLoad.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getUsers();
});
</script>

<style scoped>
.loader-overlay {
  display: flex;
  justify-content: center;

  height: 400px;
}
.active {
  background-color: var(--sin);
}
.rating-container {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
}

.rating-title {
  color: #e74c3c;
  text-align: center;
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: 600;
}

.rating-controls {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
  gap: 15px;
}

.search-input,
.filter-select {
  padding: 10px 15px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.3s;
}

.search-input {
  flex-grow: 1;
  max-width: 400px;
}

.filter-select {
  width: 200px;
}

.search-input:focus,
.filter-select:focus {
  border-color: #e74c3c;
}
.table-grid {
  display: grid;
  grid-template-columns: 50px 1fr 100px;
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.grid-header {
  display: contents;
}

.grid-header .grid-cell {
  background-color: #f8fafc;
  color: #e74c3c;
  font-weight: 600;
  padding: 12px 15px;
  border-bottom: 2px solid #e2e8f0;
}

.grid-body {
  display: contents;
}

.grid-row {
  display: contents;
}

.grid-row:hover .grid-cell {
  background-color: #f8fafc;
}

.grid-cell {
  padding: 12px 15px;
  border-bottom: 1px solid #e2e8f0;
  display: flex;
  align-items: center;
  transition: background-color 0.2s;
}

.rank-header,
.rank-cell {
  justify-content: center;
}

.user-header,
.user-cell {
  min-width: 200px;
}

.points-header,
.points-cell {
  justify-content: center;
}

.rating-header,
.rating-cell {
  justify-content: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.user-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
}

.rating-value {
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 4px;
}

.high-rating {
  color: #e74c3c;
  background-color: rgba(231, 76, 60, 0.1);
}

.medium-rating {
  color: #e67e22;
  background-color: rgba(230, 126, 34, 0.1);
}

.low-rating {
  color: #95a5a6;
  background-color: rgba(149, 165, 166, 0.1);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 15px;
  margin-top: 20px;
}

.pagination-btn {
  padding: 8px 16px;
  background-color: #e74c3c;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
}
.pagination-btn:disabled {
  background-color: #95a5a6;
}
.pagination-btn:hover :not(.pagination-btn:disabled) {
  background-color: #c0392b;
}
.pagination-btn.active {
  background-color: var(--sin);
}
.page-number {
  color: #e74c3c;
  font-size: 14px;
  font-weight: 500;
}
</style>

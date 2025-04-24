<template>
  <div class="news-controls">
    <div class="search-container">
      <input
        v-model="localFilters.searchQuery"
        placeholder="Поиск команды..."
        @input="emitFilters"
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
</template>
<script setup></script>
<style scoped>
.news-controls {
  display: flex;
  justify-content: space-around;
  align-items: center;
  margin-bottom: 2rem;
  margin-top: 2rem;
  padding: 10px;
  border-bottom: 3px solid rgb(180, 180, 180);
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
</style>

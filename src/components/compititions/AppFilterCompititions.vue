<template>
  <div class="horizontal-filter-container">
    <div class="filter-row">
      <div class="filter-item search-item">
        <div class="search-input">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Поиск..."
            @input="handleSearch"
          />
          <i class="search-icon">🔍</i>
        </div>
      </div>

      <div class="filter-item status-filter">
        <h4 class="filter-label">Статус</h4>
        <div class="filter-options">
          <label
            v-for="status in statusOptions"
            :key="status.value"
            :class="{ active: selectedStatus === status.value }"
          >
            <input
              type="radio"
              v-model="selectedStatus"
              :value="status.value"
              @change="handleStatusChange"
            />
            {{ status.label }}
          </label>
        </div>
      </div>

      <div class="filter-item region-filter">
        <h4 class="filter-label">Регион</h4>
        <select
          v-model="selectedRegion"
          @change="handleRegionChange"
          class="region-select"
        >
          <option value="">Все регионы</option>
          <option v-for="region in regions" :key="region.id" :value="region.id">
            {{ region.name }}
          </option>
        </select>
      </div>

      <div class="filter-item date-filter">
        <h4 class="filter-label">Дата</h4>
        <div class="date-inputs">
          <input
            type="date"
            v-model="startDate"
            @change="handleDateChange"
            placeholder="От"
          />
          <span>—</span>
          <input
            type="date"
            v-model="endDate"
            @change="handleDateChange"
            placeholder="До"
          />
        </div>
      </div>

      <div class="filter-item actions">
        <button class="reset-btn" @click="resetFilters">Сбросить</button>
        <button class="apply-btn" @click="applyFilters">Применить</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["filter-change"]);

const searchQuery = ref("");
const selectedStatus = ref("");
const selectedRegion = ref("");
const startDate = ref("");
const endDate = ref("");

const statusOptions = [
  { value: "active", label: "Активные" },
  { value: "pending", label: "Ожидающие" },
  { value: "completed", label: "Завершенные" },
];

const regions = [
  { id: 1, name: "Москва" },
  { id: 2, name: "Санкт-Петербург" },
  { id: 3, name: "Новосибирск" },
  // Другие регионы...
];

const handleSearch = () => {
  emit("filter-change", { search: searchQuery.value });
};

const handleStatusChange = () => {
  emit("filter-change", { status: selectedStatus.value });
};

const handleRegionChange = () => {
  emit("filter-change", { region: selectedRegion.value });
};

const handleDateChange = () => {
  emit("filter-change", {
    start_date: startDate.value,
    end_date: endDate.value,
  });
};

const applyFilters = () => {
  emit("filter-change", {
    search: searchQuery.value,
    status: selectedStatus.value,
    region: selectedRegion.value,
    start_date: startDate.value,
    end_date: endDate.value,
  });
};

const resetFilters = () => {
  searchQuery.value = "";
  selectedStatus.value = "";
  selectedRegion.value = "";
  startDate.value = "";
  endDate.value = "";
  emit("filter-change", {});
};
</script>

<style scoped>
.horizontal-filter-container {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 80%;
  margin: auto;
  display: flex;
}

.filter-row {
  margin: auto;
  display: flex;
  align-items: center;
  gap: 15px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 100px;
  flex: 1;
}

.search-item {
  min-width: 100px;
  flex: 2;
}

.filter-label {
  margin: 0 0 5px 0;
  color: #7f8c8d;
  font-size: 0.85rem;
  font-weight: 600;
  white-space: nowrap;
}

.search-input {
  flex: 1;
}

.search-input input {
  width: 90%;
  padding: 8px 8px 8px 30px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
}

.search-icon {
  position: absolute;
  left: 8px;
  top: 50%;
  transform: translateY(-50%);
  color: #7f8c8d;
  font-size: 0.9rem;
}

.filter-options {
  display: flex;
  gap: 8px;
}

.filter-options label {
  display: flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 5px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.85rem;
  white-space: nowrap;
}

.filter-options label:hover {
  background: #f5f5f5;
}

.filter-options label.active {
  background: #3498db;
  color: white;
}

.filter-options input {
  margin-right: 5px;
}

.region-select {
  width: 100%;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.9rem;
  background: white;
  color: #2c3e50;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 5px;
}

.date-inputs input {
  flex: 1;
  padding: 7px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 0.85rem;
}

.date-inputs span {
  color: #7f8c8d;
}

.actions {
  display: flex;
  gap: 10px;
  align-items: flex-end;
  min-width: 180px;
}

.reset-btn {
  padding: 8px 12px;
  background: white;
  color: #e74c3c;
  border: 1px solid #e74c3c;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  flex: 1;
}

.reset-btn:hover {
  background: #fdeaea;
}

.apply-btn {
  padding: 8px 12px;
  background: #3498db;
  color: white;
  border: none;
  border-radius: 5px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
  font-size: 0.9rem;
  flex: 1;
}

.apply-btn:hover {
  background: #2980b9;
}

@media (max-width: 992px) {
  .filter-row {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .filter-item {
    width: 100%;
  }

  .actions {
    flex-direction: row;
    margin-top: 5px;
  }
}
</style>

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
        </div>
      </div>

      <div class="filter-item status-filter">
        <h4 class="filter-label">Вид соревнований</h4>
        <div class="filter-options">
          <label
            v-for="status in formatOptions"
            :key="status.value"
            :class="{ active: selectedformat === status.value }"
          >
            <input
              type="radio"
              v-model="selectedformat"
              :value="status.value"
              @change="emitFilters"
            />
            {{ status.label }}
          </label>
        </div>
      </div>
      <div class="filter-item status-filter">
        <h4 class="filter-label">Формат соревнований</h4>
        <div class="filter-options">
          <label
            v-for="status in oflOptions"
            :key="status.value"
            :class="{ active: selectedformatOfl === status.value }"
          >
            <input
              type="radio"
              v-model="selectedformatOfl"
              :value="status.value"
              @change="emitFilters"
            />
            {{ status.label }}
          </label>
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
              @change="emitFilters"
            />
            {{ status.label }}
          </label>
        </div>
      </div>

      <div class="filter-item region-filter">
        <h4 class="filter-label">Регион</h4>
        <select
          v-model="selectedRegion"
          @change="emitFilters"
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
            @change="emitFilters"
            placeholder="От"
          />
          <span>—</span>
          <input
            type="date"
            v-model="endDate"
            @change="emitFilters"
            placeholder="До"
          />
        </div>
      </div>

      <div class="filter-item actions">
        <button class="reset-btn" @click="resetFilters">Сбросить</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref, watch } from "vue";

const emit = defineEmits(["filter-change"]);

const searchQuery = ref("");
const selectedStatus = ref("");
const selectedformat = ref("");
const selectedformatOfl = ref("");
const selectedRegion = ref("");
const startDate = ref("");
const endDate = ref("");
const props = defineProps({
  comp: Array,
});
const formatOptions = [
  { value: "individual", label: "Личное" },
  { value: "team", label: "Командное" },
];
const statusOptions = [
  { value: "registration", label: "Регистрация" },
  { value: "finished", label: "Завершены" },
];
const oflOptions = [
  { value: "online", label: "Онлайн" },
  { value: "offline", label: "Оффлайн" },
];

const handleSearch = () => {
  emitFilters();
};
const emitFilters = () => {
  console.log(selectedRegion);
  emit("filter-change", {
    search: searchQuery.value,
    status: selectedStatus.value,
    format: selectedformat.value,
    ofline: selectedformatOfl.value,
    region: selectedRegion.value,
    start_date: startDate.value,
    end_date: endDate.value,
  });
};
watch([startDate, endDate], () => {
  if (startDate.value || endDate.value) {
    emitFilters();
  }
});
const resetFilters = () => {
  searchQuery.value = "";
  selectedStatus.value = "";
  selectedRegion.value = "";
  startDate.value = "";
  endDate.value = "";
  selectedformat.value = "";
  selectedformatOfl.value = "";
  emit("filter-change", {});
};
const regions = ref();
const getRegion = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/regions/");

    regions.value = response.data;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getRegion();
});
</script>

<style scoped>
.horizontal-filter-container {
  background: white;
  border-radius: 10px;
  padding: 15px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  width: 93%;
  margin: 20px auto;
  display: flex;
}

.filter-row {
  margin: auto;
  display: flex;
  align-items: center;
  gap: 55px;
  flex-wrap: wrap;
}

.filter-item {
  display: flex;
  flex-direction: column;
  min-width: 100px;
  flex: 1;
}

.search-item {
  min-width: 130px;
  flex: 1;
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

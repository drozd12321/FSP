<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal">
      <div class="modal-header">
        <h3>Выберите вариант</h3>
        <button @click="closeModal" class="close-btn">&times;</button>
      </div>
      <div class="modal-body">
        <div class="combobox-container">
          <label for="input-field" class="combobox-label">Варианты:</label>
          <input
            id="input-field"
            type="text"
            :value="inputDisplayValue"
            @input="handleInput"
            class="combobox-input"
            placeholder="Введите или выберите"
            @focus="openDropdown"
            @blur="handleBlur"
          />
          <ul
            v-show="showDropdown && filteredOptions.length"
            class="dropdown-list"
            @mousedown.prevent
          >
            <li
              v-for="option in filteredOptions"
              :key="option.id"
              @mousedown="selectOption(option)"
            >
              {{ option.data }}
            </li>
          </ul>
        </div>
      </div>
      <button class="primary-btn" @click="sent">Отправить</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
import axios from "axios";
const props = defineProps({
  isOpen: Boolean,
});

const emit = defineEmits(["close", "select"]);

const inputDisplayValue = ref("");
const selectedId = ref(null);
const showDropdown = ref(false);
const options = ref([]);
const loading = ref();
const isData = ref();
const filteredOptions = computed(() => {
  return options.value.filter((opt) =>
    opt.data.toLowerCase().includes(inputDisplayValue.value.toLowerCase())
  );
});
const getUsers = async () => {
  try {
    loading.value = true;
    const response = await axios.get("http://10.8.0.23:8000/users/");

    if (options.value.length === 0) {
      isData.value = true;
    } else {
      isData.value = false;
    }
    options.value = response.data;
    loading.value = false;
    console.log(response.data);
    return response.data;
  } catch (error) {
    loading.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const closeModal = () => emit("close");

const handleInput = (e) => {
  inputDisplayValue.value = e.target.value;
  selectedId.value = null; // Сбрасываем выбор при ручном вводе
};

const openDropdown = () => {
  showDropdown.value = true;
};

const handleBlur = () => {
  setTimeout(() => {
    showDropdown.value = false;
  }, 200);
};

const selectOption = (option) => {
  inputDisplayValue.value = option.data;
  selectedId.value = option.id;
  showDropdown.value = false;
  console.log("Выбрано:", option.id, option.data);
};

const sent = () => {
  if (selectedId.value) {
    console.log("Отправлено ID:", selectedId.value);
    emit("select", selectedId.value);
    emit("close");
    closeModal();
  } else {
    console.warn("Не выбран ни один вариант");
  }
};
onMounted(() => {
  getUsers();
});
</script>

<style scoped>
.primary-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  margin: 20px;
}
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal {
  background: white;
  border-radius: 8px;
  width: 400px;
  max-width: 90%;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.modal-header {
  padding: 16px 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
  padding: 0;
  line-height: 1;
}

.modal-body {
  padding: 20px;
}

.combobox-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
}

.combobox-label {
  font-size: 14px;
  color: #444;
}

.combobox-input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  box-sizing: border-box;
}

.combobox-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 1px #3b82f6;
}
.dropdown-list {
  position: absolute;
  top: calc(100% + 4px);
  left: 0;
  right: 0;
  max-height: 200px;
  overflow-y: auto;
  margin: 0;
  padding: 0;
  list-style: none;
  border: 1px solid #ddd;
  border-radius: 4px;
  background: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  z-index: 10;
}
.dropdown-list li {
  padding: 8px 12px;
  cursor: pointer;
  font-size: 14px;
}

.dropdown-list li:hover {
  background-color: #f5f5f5;
}
</style>

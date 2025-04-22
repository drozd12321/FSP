<template>
  <div>
    <div v-if="loading" class="loader-overlay"><Loader /></div>
    <div class="competition-form">
      <h2>Создание нового соревнования</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Название соревнования</label>
          <input v-model="form.name" required />
        </div>
        <div class="form-group">
          <label>Дисциплина</label>
          <select v-model="form.discipline" required>
            <option v-for="dicp in distiplines" :value="dicp.id">
              {{ dicp.name }}
            </option>
          </select>
        </div>
        <div class="form-group">
          <label>Описание</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Макс. участников</label>
            <input
              type="number"
              v-model.number="form.max_participants"
              required
            />
          </div>
          <div class="form-group">
            <label>Макс. в команде</label>
            <input
              type="number"
              v-model.number="form.max_participants_in_team"
              required
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Минимальный возраст</label>
            <input
              min="10"
              max="50"
              type="number"
              v-model.number="form.min_age"
              required
            />
          </div>

          <div class="form-group">
            <label>Максимальный возраст</label>
            <input type="number" v-model.number="form.max_age" required />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group">
            <label>Тип проведения</label>
            <select v-model="form.competition_type" required>
              <option value="offline">Оффлайн</option>
              <option value="online">Онлайн</option>
            </select>
          </div>
          <div class="form-group">
            <label>Формат</label>
            <select v-model="form.type" required>
              <option value="individual">Индивидуальный</option>
              <option value="team">Командный</option>
            </select>
          </div>
        </div>
        <div class="form-group">
          <label>Доступные регионы</label>
          <div class="regions-controls">
            <button
              type="button"
              @click="toggleAllRegions"
              class="select-all-btn"
            >
              {{ allRegionsSelected ? "Снять все" : "Выбрать все" }}
            </button>
            <span class="selected-count">
              Выбрано: {{ form.permissions.length }} из
              {{ russianRegions.length }}
            </span>
          </div>
          <multiselect
            v-model="form.permissions"
            :options="russianRegions"
            :multiple="true"
            :close-on-select="false"
            placeholder="Выберите регионы"
            label="name"
            track-by="code"
          ></multiselect>
        </div>
        <div class="form-group">
          <label>Даты проведения</label>
          <div class="date-inputs">
            <input
              type="datetime-local"
              v-model="form.dates.start_date"
              required
            />
            <span>до</span>
            <input
              type="datetime-local"
              v-model="form.dates.end_date"
              required
            />
          </div>
        </div>
        <div class="form-group">
          <label>Даты регистрации*</label>
          <div class="date-inputs">
            <input
              type="datetime-local"
              v-model="form.dates.registration_start"
              required
            />
            <span>до</span>
            <input
              type="datetime-local"
              v-model="form.dates.registration_end"
              required
            />
          </div>
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          Создать соревнование
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import Multiselect from "vue-multiselect";
import Loader from "./Loader.vue";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
import axios from "axios";
const compStore = competitionStore();
const { loading } = storeToRefs(competitionStore());
const distiplines = ref();
const russianRegions = ref([
  { code: "RU-MOW", name: "Москва" },
  { code: "RU-SPE", name: "Санкт-Петербург" },
  { code: "RU-MOS", name: "Московская область" },
]);
const form = ref({
  name: "",
  discipline: "",
  description: "",
  max_participants: 100,
  max_participants_in_team: 4,
  min_age: 10,
  max_age: 60,
  competition_type: "offline",
  type: "team",
  status: "upcoming",
  permissions: [],
  dates: {
    start_date: "",
    end_date: "",
    registration_start: "",
    registration_end: "",
  },
});

const handleSubmit = async () => {
  const formattedData = {
    ...form.value,
    dates: {
      start_date: new Date(form.value.dates.start_date).toISOString(),
      end_date: new Date(form.value.dates.end_date).toISOString(),
      registration_start: new Date(
        form.value.dates.registration_start
      ).toISOString(),
      registration_end: new Date(
        form.value.dates.registration_end
      ).toISOString(),
    },
  };
  console.log("Отправка данных:", formattedData);
  const response = await compStore.addCompetitions(formattedData);
  console.log("Отправка данных:", formattedData);
  console.log("Отправка данных:", response);
};
const allRegionsSelected = computed(() => {
  return form.value.permissions.length === russianRegions.value.length;
});
const toggleAllRegions = () => {
  if (allRegionsSelected.value) {
    form.value.permissions = [];
  } else {
    form.value.permissions = [...russianRegions.value];
  }
};
const getDisciplin = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/disciplines/");

    distiplines.value = response.data;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getDisciplin();
});
</script>

<style scoped>
h2 {
  color: var(--sin);
}
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1000;
}
.select-all-btn {
  background: none;
  border: none;
  color: #3b82f6;
  cursor: pointer;
  padding: 4px 8px;
  font-size: 0.9rem;
}
.select-all-btn:hover {
  text-decoration: underline;
}
.competition-form {
  max-width: 800px;
  margin: 10px auto;
  border-radius: 7px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(3, 3, 3, 0.5);
}
.form-group {
  margin-bottom: 1rem;
  width: 100%;
}
.form-row {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}
.form-row .form-group {
  display: grid;
  grid-template-columns: repeat(2, fr);
}
label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input,
textarea,
select {
  width: 95%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  box-shadow: none;
}
select {
  background-color: white;
}
textarea {
  resize: none;
}
input:focus,
textarea:focus,
select:focus {
  border: 2px solid #3b82f6;
}

.date-inputs input {
  flex: 1;
}

.submit-btn {
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
}

.submit-btn:hover {
  background-color: #2563eb;
}
</style>

<style src="vue-multiselect/dist/vue-multiselect.css"></style>

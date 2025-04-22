<template>
  <div class="competition-form">
    <h2>Создание нового соревнования</h2>

    <form @submit.prevent="handleSubmit">
      <div class="form-group">
        <label>Название соревнования*</label>
        <input v-model="form.name" required />
      </div>

      <div class="form-group">
        <label>Дисциплина</label>
        <input v-model="form.discipline.name" required />
      </div>

      <div class="form-group">
        <label>Описание</label>
        <textarea v-model="form.description"></textarea>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Макс. участников*</label>
          <input
            type="number"
            v-model.number="form.max_participants"
            required
          />
        </div>
        <div class="form-group">
          <label>Макс. в команде*</label>
          <input
            type="number"
            v-model.number="form.max_participants_in_team"
            required
          />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Минимальный возраст*</label>
          <input type="number" v-model.number="form.min_age" required />
        </div>

        <div class="form-group">
          <label>Максимальный возраст*</label>
          <input type="number" v-model.number="form.max_age" required />
        </div>
      </div>
      <div class="form-row">
        <div class="form-group">
          <label>Тип проведения</label>
          <select v-model="form.competition_type" required>
            <option value="offline">Оффлайн</option>
            <option value="online">Онлайн</option>
            <option value="hybrid">Гибрид</option>
          </select>
        </div>

        <div class="form-group">
          <label>Формат*</label>
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
          required
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
          <input type="datetime-local" v-model="form.dates.end_date" required />
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

      <button type="submit" class="submit-btn">Создать соревнование</button>
    </form>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import Multiselect from "vue-multiselect";

const russianRegions = ref([
  { code: "RU-MOW", name: "Москва" },
  { code: "RU-SPE", name: "Санкт-Петербург" },
  { code: "RU-MOS", name: "Московская область" },
]);

const form = ref({
  name: "",
  discipline: { name: "" },
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

const handleSubmit = () => {
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
const isRegionSelected = (code) => {
  return form.value.permissions.some((region) => region.code === code);
};
</script>

<style scoped>
.competition-form {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-row {
  display: flex;
  gap: 1rem;
}

.form-row .form-group {
  flex: 1;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input,
textarea,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.date-inputs {
  display: flex;
  align-items: center;
  gap: 1rem;
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

<template>
  <div>
    <div v-if="loading" class="loader-overlay"><Loader /></div>
    <div class="competition-form">
      <h2>Создание новой команды</h2>
      <form @submit.prevent="handleSubmit">
        <div class="form-group">
          <label>Название команды</label>
          <input
            type="text"
            v-model="form.name"
            required
            placeholder="Введите название команды"
          />
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          Создать команду
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import Loader from "./Loader.vue";
import axios from "axios";

const loading = ref(false);
const form = ref({
  competition_id: null,
  name: "",
  captain_id: null,
});

const handleSubmit = async () => {
  try {
    loading.value = true;
    const response = await axios.post(
      "http://10.8.0.23:8000/teams/",
      form.value
    );
    console.log("Команда создана:", response.data);
  } catch (error) {
    console.error("Ошибка при создании команды:", error);
  } finally {
    loading.value = false;
  }
};
</script>
<style scoped>
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

.competition-form {
  max-width: 500px;
  margin: 10px auto;
  border-radius: 7px;
  padding: 2rem;
  box-shadow: 0 0 12px rgba(3, 3, 3, 0.5);
}

.form-group {
  margin-bottom: 1.5rem;
  width: 100%;
}

label {
  display: block;
  margin-bottom: 0.5rem;
  font-weight: 500;
}

input,
select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  box-shadow: none;
}

input:focus,
select:focus {
  border: 2px solid #3b82f6;
}

.submit-btn {
  background-color: #3b82f6;
  color: white;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 1rem;
  width: 100%;
  margin-top: 1rem;
}

.submit-btn:hover {
  background-color: #2563eb;
}

.submit-btn:disabled {
  background-color: #93c5fd;
  cursor: not-allowed;
}
</style>

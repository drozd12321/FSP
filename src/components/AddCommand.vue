<template>
  {{ form }}
  <div>
    <div v-if="loading" class="loader-overlay"><Loader /></div>
    <div class="competition-form">
      <h2>Создание новой команды</h2>
      <form @submit.prevent="createCommand">
        <div class="form-group">
          <label>Название команды</label>
          <input
            type="text"
            v-model="form.name"
            required
            placeholder="Введите название команды"
          />
        </div>
        <div class="form-group">
          <label class="label" for="email">Вид команды</label>
          <select name="comand" id="comand" v-model="comand">
            <option value="0">Публичная</option>
            <option value="1">Приватная</option>
          </select>
        </div>
        <div class="form-group">
          <label class="label" for="email">Описание</label>
          <textarea v-model="form.description"></textarea>
        </div>
        <button type="submit" class="submit-btn" :disabled="loading">
          Создать команду
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import Loader from "./Loader.vue";
import axios from "axios";
import { useAuthStore } from "@/stores/useAuthStore";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
const { getUser } = storeToRefs(useAuthStore());
const comand = ref("");
const loading = ref(false);
const form = ref({
  competition: null,
  name: "",
  is_prived: null,
  description: "",
});
const createCommand = () => {
  if (comand.value === "0") {
    form.value.is_prived = true;
  } else {
    form.value.is_prived = false;
  }
};
</script>
<style scoped>
textarea {
  width: 95%;
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  box-shadow: none;
  resize: none;
}
h2 {
  color: #e74c3c;
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

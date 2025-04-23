<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div v-if="getLoading" class="loader-overlay"><Loader /></div>
      <div class="competition-form">
        <button class="close-btn" @click="closeModal">×</button>
        <h2>
          {{
            type === "Командное" ? "Создание новой команды" : "Подтверждение"
          }}
        </h2>
        <form @submit.prevent="createCommand">
          <div v-if="type === 'Командное'" class="form-group">
            <label>Название команды</label>
            <input
              type="text"
              v-model="form.name"
              required
              placeholder="Введите название команды"
            />
          </div>
          <div v-if="type === 'Командное'" class="form-group">
            <label class="label" for="email">Вид команды</label>
            <select name="comand" id="comand" v-model="comand">
              <option value="0">Публичная</option>
              <option value="1">Приватная</option>
            </select>
          </div>
          <div v-if="type === 'Командное'" class="form-group">
            <label class="label" for="email">Описание</label>
            <textarea v-model="form.description"></textarea>
          </div>
          <button
            v-if="type === 'Командное'"
            type="submit"
            class="submit-btn"
            :disabled="loading"
          >
            Регистрация новой команды
          </button>
          <div v-if="type" class="two">
            <button
              v-if="type === 'Личное'"
              type="submit"
              class="submit-btn"
              :disabled="loading"
            >
              Подтвердить
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import Loader from "./Loader.vue";
import { useCommandStore } from "@/stores/storeCommand";
import { storeToRefs } from "pinia";
const { getLoading, getId, getType } = storeToRefs(useCommandStore());
const comStore = useCommandStore();
const emit = defineEmits(["close"]);
const comand = ref("");
const form = ref({
  competition: null,
  name: "",
  is_private: null,
  description: "",
});
const formU = ref({
  competition: null,
});
const idd = computed(() => {
  return getId.value;
});
const type = computed(() => {
  return getType.value;
});
const token = ref();
const user = ref();
const createCommand = async (action) => {
  if (type.value === "Командное") {
    console.log(token.value);
    if (comand.value === "0") {
      form.value.is_private = true;
    } else {
      form.value.is_private = false;
    }
    form.value.competition = idd.value;
    await comStore.addCommand(
      "http://10.8.0.23:8000/teams/",
      form.value,
      token.value
    );
    console.log(form.value);
  } else {
    formU.value.competition = idd.value;
    await comStore.addCommand(
      "http://10.8.0.23:8000/user-applications/",
      formU.value,
      token.value
    );
  }
  console.log(formU.value);
  resetForm();
};
const resetForm = () => {
  if (type === "Командное") {
    form.value = {
      competition: null,
      name: "",
      is_private: null,
      description: "",
    };
  } else {
    formU.value = {
      competition: null,
    };
  }
};
const closeModal = () => {
  emit("close");
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken");
  user.value = JSON.parse(localStorage.getItem("user"));
});
</script>

<style scoped>
.submit-btn.two {
  background-color: #e74c3c;
}
.two {
  display: flex;
  gap: 10px;
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

.modal-content {
  position: relative;
  background: white;
  border-radius: 8px;
  max-width: 500px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
}

.close-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #666;
}

.close-btn:hover {
  color: #e74c3c;
}

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
  margin-top: 10px;
}

.loader-overlay {
  display: flex;
  justify-content: center;

  height: 100px;
}

.competition-form {
  padding: 2rem;
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

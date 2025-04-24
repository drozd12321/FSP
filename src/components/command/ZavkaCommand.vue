<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <div v-if="loading" class="loader-overlay"><Loader /></div>
      <div class="competition-form">
        <button class="close-btn" @click="closeModal">×</button>
        <h2>Заявка на присоединение к команде</h2>
        <form @submit.prevent="createCommand">
          <div class="form-group">
            <label>Текст отклика</label>
            <textarea
              name="description"
              id="description"
              v-model="form.description"
              placeholder="Расскажите о себе"
              required
            ></textarea>
          </div>
          <button type="submit" class="submit-btn" :disabled="loading">
            Присоединиться к команде
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import { useCommandStore } from "@/stores/storeCommand";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
import Loader from "../Loader.vue";
const comStore = useCommandStore();
const { getId, getteamId } = storeToRefs(competitionStore());
const emit = defineEmits(["close"]);
const loading = ref(false);
const form = ref({
  id: "",
  description: "",
  team_id: "",
});
const id = computed(() => {
  return getId.value;
});
const teamId = computed(() => {
  return getteamId.value;
});
const token = ref();
const createCommand = async () => {
  loading.value = true;
  form.value.id = id.value;
  form.value.team_id = teamId.value;
  await comStore.addCommand(
    "http://10.8.0.23:8000/response-to-public/",
    form.value,
    token.value
  );
  loading.value = false;
  console.log(form.value);
  resetForm();
};
const resetForm = () => {
  form.value = {
    id: "",
    description: "",
  };
};
const closeModal = () => {
  emit("close");
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken");
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
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 10;
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

<template>
  <div class="compact-competition-card" @click="toggleDetails">
    <div class="card-header">
      <div class="card-badge">{{ disciplineName }}</div>
      <h3 class="card-title">{{ name }}</h3>
    </div>

    <div class="card-dates">
      <div class="date-item">
        <RegisterIcon class="icon" />
        <span>{{ useStatus(status) }}</span>
      </div>
    </div>

    <div v-if="type" class="card-footer">
      <div class="card-type">
        <span> Тип проведения: </span>
      </div>
      <button class="details-btn">
        {{ type === "team" ? "Командное" : "Личное" }}
      </button>
    </div>
    <div v-if="res" class="card-footer">
      <div class="card-type">
        <span> Mecто: </span>
      </div>
      <button class="details-btn">
        {{ res }}
      </button>
    </div>
    <div class="card-footer">
      <div class="card-type">
        <span> Оценка: </span>
      </div>
      <button class="details-btn">
        {{ rated ? "Оценено" : "Не оценено" }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";
import CalendarIcon from "../utils/icons/CalendarIcon.vue";
import RegisterIcon from "../utils/icons/RegisterIcon.vue";
const props = defineProps({
  name: String,
  disciplineName: String,
  status: String,
  type: String,
  res: Number,
  rated: Boolean,
});

const showDetails = ref(false);
const registrationOpen = computed(() => props.status === "registration");
const useStatus = (st) => {
  if (st === "finished") {
    return "Завершено";
  }
  if (st === "registration") {
    return "Регистрация";
  }
  if (st === "running") {
    return "Идет сейчас";
  }
  if (st === "waiting") {
    return "В ожидании";
  }
};
const toggleDetails = () => {
  showDetails.value = !showDetails.value;
};
</script>

<style scoped>
.compact-competition-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 16px;
  margin-left: 19rem;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 4px solid var(--sin);
  max-width: 1100px;
}

.compact-competition-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  transform: translateY(-2px);
}

.card-header {
  margin-bottom: 12px;
  position: relative;
}

.card-badge {
  position: absolute;
  top: -12px;
  right: 0;
  background-color: var(--sin);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.7rem;
  font-weight: 600;
}

.card-title {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
  padding-right: 60px;
}

.card-dates {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
}

.date-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.9rem;
  color: #7f8c8d;
}

.icon {
  width: 16px;
  height: 16px;
  color: var(--sin);
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-type {
  font-size: 0.85rem;
  color: #95a5a6;
  font-style: italic;
}

.details-btn {
  background: none;
  border: none;
  color: var(--sin);
  font-weight: 600;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.details-btn:hover {
  background-color: rgba(231, 76, 60, 0.1);
}

.card-details {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid #eee;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.detail-label {
  color: #7f8c8d;
  font-weight: 500;
}

/* Анимации */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.2s ease-in;
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

@media (max-width: 768px) {
  .card-title {
    font-size: 1.1rem;
  }

  .card-dates {
    flex-direction: column;
    gap: 8px;
  }
}
</style>

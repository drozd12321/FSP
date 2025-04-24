<template>
  <div class="application-card">
    <div class="card-header">
      <h3 v-if="name" class="card-title">{{ name }}</h3>
      <h3 v-if="teamName" class="card-title">{{ teamName }}</h3>
      <span
        v-if="competition_type_display"
        class="card-status"
        :class="statusClass"
        >{{ competition_type_display }}</span
      >
      <span
        v-if="status"
        class="card-status"
        :class="{
          danger: status === 'Отклонено',
          primary: status === 'Одобрено',
          warning: status === 'В рассмотрении',
        }"
        >{{ status }}</span
      >
    </div>

    <div class="card-content">
      <div v-if="competition_type_display" class="info-row">
        <span class="info-label"> Формат:</span>
        <span class="info-value">{{ competition_type_display }}</span>
      </div>
      <div v-if="competitionName" class="info-row">
        <span class="info-label"> Название соревнований:</span>
        <span class="info-value">{{ competitionName }}</span>
      </div>
      <div v-if="!discipline_name">
        <div v-if="type_display" class="info-row">
          <span class="info-label">Тип:</span>
          <span class="info-value">{{ type_display }}</span>
        </div>
        <div v-if="userName" class="info-row">
          <span class="info-label">ФИО:</span>
          <span class="info-value"
            >{{ userName }} {{ userSurname }} - '{{ userNickname }}'</span
          >
        </div>

        <div v-if="startDate" class="info-row">
          <span class="info-label">Даты проведения:</span>
          <span class="info-value">{{
            formatDateRange(startDate, endDate)
          }}</span>
        </div>
        <div class="info-row descr">
          <span class="info-label">Описание:</span>
          <span class="info-value">{{ description }}</span>
        </div>
      </div>
      <div v-else>
        <div class="info-row">
          <span class="info-label">Название дисциплины:</span>
          <span class="info-value">{{ discipline_name }}</span>
        </div>
      </div>
    </div>

    <div v-if="!discipline_name" class="card-actions">
      <button class="action-btn reject-btn" @click="reject">Отклонить</button>
      <button class="action-btn approve-btn" @click="approve">
        Подтвердить
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from "vue";
import formatDateRange from "@/use/useFilterData";
import axios from "axios";
const emit = defineEmits([
  "approveApplication",
  "rejectApplication",
  "acceptvacancyresponse",
  "rejectvacancyresponse",
]);
const props = defineProps({
  name: String,
  competition_type_display: String,
  type_display: String,
  discipline_name: String,
  startDate: String,
  endDate: String,
  description: String,
  id: Number,
  status: String,
  teamName: String,
  competitionName: String,
  userName: String,
  userSurname: String,
  userNickname: String,
});
const token = ref();
onMounted(() => {
  token.value = localStorage.getItem("jwtToken");
});
const reject = () => {
  emit("rejectApplication", props.id);
  emit("rejectvacancyresponse", props.id);
};
const approve = () => {
  emit("approveApplication", props.id);
  emit("acceptvacancyresponse", props.id);
};
</script>

<style scoped>
.application-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 10px;
  margin-bottom: 16px;
  border-left: 4px solid var(--sin);
  transition: all 0.3s ease;
  border-bottom: 1px solid rgb(158, 157, 157);
}

.application-card:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eaeaea;
}

.card-title {
  margin: 0;
  font-size: 1.2rem;
  color: #2c3e50;
  font-weight: 600;
}

.card-status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
}
.card-status.primary {
  color: white;
  background-color: #166534;
}
.card-status.danger {
  color: white;
  background-color: #ef4444;
}
.card-status.warning {
  color: white;
  background-color: #2563eb;
}
.status-pending {
  background-color: #fef9c3;
  color: #854d0e;
}

.status-approved {
  background-color: #dcfce7;
  color: #166534;
}

.status-rejected {
  background-color: #fee2e2;
  color: #991b1b;
}

.card-content {
  margin-bottom: 16px;
}

.info-row {
  display: grid;
  grid-template-columns: 300px auto;
  margin-bottom: 8px;
}
.info-row.descr {
  max-width: 700px;
}
.info-label {
  font-weight: 500;
  color: #7f8c8d;
  min-width: 120px;
}

.info-value {
  color: #2c3e50;
}

.card-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 12px;
  border-top: 1px solid #eaeaea;
}

.action-btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
  font-size: 0.9rem;
}

.approve-btn {
  background-color: #3b82f6;
  color: white;
}

.approve-btn:hover {
  background-color: #2563eb;
}

.reject-btn {
  background-color: #f8f9fa;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.reject-btn:hover {
  background-color: #fee2e2;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .card-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>

<template>
  <div class="application-card">
    <div class="card-header">
      <h3 class="card-title">{{ application.title }}</h3>
      <span class="card-status" :class="statusClass">{{
        application.status
      }}</span>
    </div>

    <div class="card-content">
      <div class="info-row">
        <span class="info-label">Участник:</span>
        <span class="info-value">{{ application.userName }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Дата подачи:</span>
        <span class="info-value">{{ formatDate(application.submitDate) }}</span>
      </div>
      <div class="info-row">
        <span class="info-label">Команда:</span>
        <span class="info-value">{{
          application.teamName || "Индивидуально"
        }}</span>
      </div>
    </div>

    <div class="card-actions">
      <button class="action-btn reject-btn" @click="rejectApplication">
        Отклонить
      </button>
      <button class="action-btn approve-btn" @click="approveApplication">
        Подтвердить
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

const props = defineProps({
  application: {
    type: Object,
    required: true,
    default: () => ({
      id: 0,
      title: "Название заявки",
      userName: "Иван Иванов",
      teamName: "Команда А",
      submitDate: new Date().toISOString(),
      status: "на рассмотрении", // 'на рассмотрении', 'подтверждена', 'отклонена'
    }),
  },
});

const emit = defineEmits(["approve", "reject"]);

const statusClass = computed(() => {
  return {
    "status-pending": props.application.status === "на рассмотрении",
    "status-approved": props.application.status === "подтверждена",
    "status-rejected": props.application.status === "отклонена",
  };
});

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString("ru-RU");
};

const approveApplication = () => {
  emit("approve", props.application.id);
};

const rejectApplication = () => {
  emit("reject", props.application.id);
};
</script>

<style scoped>
.application-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 20px;
  margin-bottom: 16px;
  border-left: 4px solid var(--sin);
  transition: all 0.3s ease;
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
  display: flex;
  margin-bottom: 8px;
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
  padding-top: 16px;
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

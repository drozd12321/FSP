<template>
  <div v-if="act"><AppMsg :act="act" /></div>
  <div class="message-card">
    <div class="card-header">
      <h3 class="card-title">
        Вам пришло приглашение от команды {{ teamName }}
      </h3>
    </div>

    <div class="card-content">
      <div class="message-text">Название соревнования: {{ teamName }}</div>
      <div class="message-text">Статус: {{ status }}</div>
    </div>

    <div class="card-actions">
      <button class="primary-btn" @click="sentPochta('accept')">Да</button>
      <button class="primary-danger" @click="sentPochta('reject')">Нет</button>
    </div>
  </div>
</template>

<script setup>
import { useMsgStore } from "@/stores/useMessageStore";
import axios from "axios";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
import AppMsg from "../message/AppMsg.vue";

const props = defineProps({
  name: String,
  status: String,
  teamName: String,
  id: Number,
});
const emit = defineEmits(["feh"]);
const msgStore = useMsgStore();
const { getMsg } = storeToRefs(useMsgStore());
const loading = ref(false);
const izavka = ref();
const isData = ref(false);
const token = ref();
const act = computed(() => {
  return getMsg.value;
});
const sentPochta = async (action) => {
  try {
    loading.value = true;
    const response = await axios.patch(
      `http://10.8.0.23:8000/invitations/${props.id}/respond/`,
      { action: action },
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    izavka.value = response.data;
    console.log(response);
    if (izavka.value.length === 0) {
      isData.value = true;
    } else {
      isData.value = false;
    }
    msgStore.setMesg({
      show: true,
      type: "succses",
      title: response.status,
    });

    loading.value = false;
    console.log("zavka", izavka.value);
    emit("feh");
    return response.data;
  } catch (error) {
    msgStore.setMesg({
      show: true,
      type: "succses",
      title: error.response.data[0],
    });
    isData.value = true;
    loading.value = false;
    console.error("Error fetching regions:", error);
    emit("feh");
    throw error;
  }
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken").trim();
});
</script>

<style scoped>
.primary-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  height: 40px;
}
.primary-btn:hover {
  background-color: #2563eb;
  transform: translateY(-2px);
}
.primary-danger:hover {
  background: #c0392b;
  transform: translateY(-2px);
}
.primary-danger {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 10px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  min-width: 120px;
  height: 40px;
}
.message-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.08);
  padding: 16px;
  margin-bottom: 16px;
  border-left: 4px solid var(--sin);
  transition: all 0.3s ease;
  max-width: 600px;
  border-bottom: 2px solid rgb(185, 185, 185);
}

.message-card:hover {
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  padding-bottom: 12px;
  border-bottom: 1px solid #eaeaea;
  flex-wrap: wrap;
  gap: 8px;
}

.card-title {
  margin: 0;
  font-size: 1.1rem;
  color: #2c3e50;
  font-weight: 600;
  order: 1;
}

.card-status {
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.75rem;
  font-weight: 600;
  order: 3;
}

.message-time {
  font-size: 0.8rem;
  color: #7f8c8d;
  order: 2;
}

.status-regular {
  background-color: #f3f4f6;
  color: #374151;
}

.status-system {
  background-color: #e0f2fe;
  color: #0369a1;
}

.status-alert {
  background-color: #fee2e2;
  color: #b91c1c;
}

.status-success {
  background-color: #dcfce7;
  color: #166534;
}

.status-warning {
  background-color: #fef9c3;
  color: #854d0e;
}

.card-content {
  margin-bottom: 12px;
}

.message-text {
  color: #2c3e50;
  line-height: 1.5;
  margin-bottom: 12px;
}

.message-attachments {
  margin-top: 12px;
  border-top: 1px dashed #eaeaea;
  padding-top: 12px;
}

.attachment {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 0.9rem;
}

.attachment-icon {
  color: #7f8c8d;
}

.attachment-name {
  color: #3b82f6;
  text-decoration: underline;
  cursor: pointer;
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

.primary-btn {
  background-color: #3b82f6;
  color: white;
}

.primary-btn:hover {
  background-color: #2563eb;
}

.secondary-btn {
  background-color: #f8f9fa;
  color: #4b5563;
  border: 1px solid #d1d5db;
}

.secondary-btn:hover {
  background-color: #f3f4f6;
}

.danger-btn {
  background-color: #f8f9fa;
  color: #ef4444;
  border: 1px solid #ef4444;
}

.danger-btn:hover {
  background-color: #fee2e2;
}

@media (max-width: 768px) {
  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .card-title {
    order: 1;
  }

  .message-time {
    order: 2;
  }

  .card-status {
    order: 3;
  }

  .card-actions {
    flex-direction: column;
  }

  .action-btn {
    width: 100%;
  }
}
</style>

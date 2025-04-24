<template>
  <div
    class="notification"
    :class="{
      show: act.show,
      primary: act.type === 'succses',
      danger: act.type === 'error',
    }"
  >
    <div
      class="notification-content"
      :class="{
        primary: act.type === 'succses',
        danger: act.type === 'error',
      }"
    >
      <div class="icon-wrapper">
        <svg
          v-if="act.type === 'succses'"
          class="check-icon"
          viewBox="0 0 24 24"
        >
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
        </svg>
        <svg v-else class="check-icon" viewBox="0 0 24 24">
          <path
            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm5 13.59L15.59 17 12 13.41 8.41 17 7 15.59 10.59 12 7 8.41 8.41 7 12 10.59 15.59 7 17 8.41 13.41 12 17 15.59z"
            fill="#e74c3c"
          />
        </svg>
      </div>
      <div class="text-content">
        <h3 class="title">{{ act.type === "error" ? "Ошибка" : "Успешно" }}</h3>
        <p class="message">{{ act.title }}</p>
      </div>
      <button class="close-btn" @click="hideNotification">
        <svg class="close-icon" viewBox="0 0 24 24">
          <path
            d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
          />
        </svg>
      </button>
    </div>
  </div>
</template>

<script setup>
import { onUnmounted, ref, watch } from "vue";
import { useCommandStore } from "@/stores/storeCommand";
import { useAuthStore } from "@/stores/useAuthStore";
import { useMsgStore } from "@/stores/useMessageStore";
const commandStore = useCommandStore();
const authStore = useAuthStore();
const msgError = useMsgStore();
const props = defineProps({
  act: Object,
  message: {
    type: String,
    default: "Действие выполнено успешно",
  },
  duration: {
    type: Number,
    default: 5000,
  },
});

const isVisible = ref(false);

const showNotification = () => {
  isVisible.value = true;
  setTimeout(() => {
    isVisible.value = false;
  }, props.duration);
};
let timeoutId = null;
const hideNotification = () => {
  commandStore.setMesg({ show: false, type: "", title: "" });
  authStore.setMesg({ show: false, type: "", title: "" });
  msgError.setMesg({ show: false, type: "", title: "" });
};
watch(
  () => props.act.show,
  (show) => {
    if (show) {
      timeoutId = setTimeout(() => {
        hideNotification();
      }, props.duration);
    } else {
      clearTimeout(timeoutId);
    }
  }
);
onUnmounted(() => {
  clearTimeout(timeoutId);
});
defineExpose({
  showNotification,
  hideNotification,
});
</script>

<style scoped>
.notification {
  position: fixed;
  top: 20px;
  right: 20px;
  transform: translateX(150%);
  transition: transform 0.3s ease-in-out;
  z-index: 1000;
  width: 350px;
  max-width: 90%;
}

.notification.show {
  transform: translateX(0);
}

.notification-content {
  display: flex;
  align-items: center;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
}
.notification-content.danger {
  background: #fee2e2;
}
.notification-content.primary {
  background: #f0fdf4;
}
.notification.primary {
  border-left: 4px solid #10b981;
  border-radius: 8px;
}
.notification.danger {
  border-left: 4px solid #d30420;
  border-radius: 8px;
}
.icon-wrapper {
  margin-right: 12px;
  flex-shrink: 0;
}

.check-icon {
  width: 24px;
  height: 24px;
  fill: #10b981;
}

.text-content {
  flex-grow: 1;
}

.title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  color: #065f46;
}

.message {
  margin: 0;
  font-size: 14px;
  color: #047857;
  line-height: 1.4;
}

.close-btn {
  background: none;
  border: none;
  margin-left: 12px;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s;
}

.close-btn:hover {
  background-color: rgba(16, 185, 129, 0.1);
}

.close-icon {
  width: 20px;
  height: 20px;
  fill: #065f46;
  opacity: 0.7;
  transition: opacity 0.2s;
}

.close-btn:hover .close-icon {
  opacity: 1;
}
@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}
@keyframes slideOut {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(150%);
  }
}

.notification.show {
  animation: slideIn 0.3s forwards;
}

.notification:not(.show) {
  animation: slideOut 0.3s forwards;
}
</style>

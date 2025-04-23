<template>
  <div class="notification" :class="{ show: act.show }">
    <div class="notification-content">
      <div class="icon-wrapper">
        <svg class="check-icon" viewBox="0 0 24 24">
          <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z" />
        </svg>
      </div>
      <div class="text-content">
        <h3 class="title">Успешно!</h3>
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
const commandStore = useCommandStore();
const authStore = useAuthStore();
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
  background: #f0fdf4;
  border-left: 4px solid #10b981;
  border-radius: 8px;
  padding: 16px;
  box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
    0 2px 4px -1px rgba(0, 0, 0, 0.06);
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

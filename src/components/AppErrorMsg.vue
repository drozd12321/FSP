<template>
  <transition name="slide-fade">
    <div
      v-if="visible"
      class="error-notification"
      :class="type"
      @click="dismiss"
    >
      <div class="error-content">
        <svg class="error-icon" viewBox="0 0 24 24" v-if="!hideIcon">
          <path
            fill="currentColor"
            d="M12,2C17.53,2 22,6.47 22,12C22,17.53 17.53,22 12,22C6.47,22 2,17.53 2,12C2,6.47 6.47,2 12,2M15.59,7L12,10.59L8.41,7L7,8.41L10.59,12L7,15.59L8.41,17L12,13.41L15.59,17L17,15.59L13.41,12L17,8.41L15.59,7Z"
          />
        </svg>
        <div class="text-content">
          <h4 class="error-title" v-if="title">{{ title }}</h4>
          <p class="error-message">{{ message }}</p>
        </div>
        <button v-if="dismissable" class="close-btn" @click.stop="dismiss">
          <svg viewBox="0 0 24 24" width="18" height="18">
            <path
              fill="currentColor"
              d="M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"
            />
          </svg>
        </button>
      </div>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch, computed } from "vue";

const props = defineProps({
  title: String,
  message: String,
  type: {
    type: String,
    default: "error",
    validator: (value) =>
      ["error", "warning", "success", "info"].includes(value),
  },
  timeout: {
    type: Number,
    default: 5000,
  },
  dismissable: {
    type: Boolean,
    default: true,
  },
  hideIcon: Boolean,
});

const emit = defineEmits(["dismissed"]);
const visible = ref(true);

let timeoutId;

const dismiss = () => {
  visible.value = false;
  emit("dismissed");
  if (timeoutId) clearTimeout(timeoutId);
};

watch(
  () => props.timeout,
  (newTimeout) => {
    if (newTimeout > 0) {
      if (timeoutId) clearTimeout(timeoutId);
      timeoutId = setTimeout(dismiss, newTimeout);
    }
  },
  { immediate: true }
);

const typeClasses = computed(() => ({
  error: props.type === "error",
  warning: props.type === "warning",
  success: props.type === "success",
  info: props.type === "info",
}));
</script>

<style scoped>
.error-notification {
  position: relative;
  width: 100%;
  max-width: 480px;
  margin: 0 auto 16px;
  padding: 16px 20px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.96);
  border-left: 4px solid;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  overflow: hidden;
  z-index: 1000;
}

.error-notification:hover {
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.error-content {
  display: flex;
  align-items: flex-start;
  gap: 12px;
}

.error-icon {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  margin-top: 2px;
}

.text-content {
  flex-grow: 1;
}

.error-title {
  margin: 0 0 4px 0;
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
}

.error-message {
  margin: 0;
  font-size: 14px;
  line-height: 1.5;
  opacity: 0.9;
}

.close-btn {
  background: none;
  border: none;
  padding: 0;
  margin-left: 8px;
  cursor: pointer;
  opacity: 0.6;
  transition: opacity 0.2s;
}

.close-btn:hover {
  opacity: 1;
}

/* Цветовые схемы */
.error {
  border-color: #ff4d4f;
  color: #ff4d4f;
}

.warning {
  border-color: #faad14;
  color: #faad14;
}

.success {
  border-color: #52c41a;
  color: #52c41a;
}

.info {
  border-color: #1890ff;
  color: #1890ff;
}

/* Анимации */
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from,
.slide-fade-leave-to {
  transform: translateY(-20px);
  opacity: 0;
}
</style>

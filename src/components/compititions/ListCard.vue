<template>
  <div class="competition-card" :class="{ expanded: allInfo }">
    <div class="card-header">
      <h2 class="card-title">{{ name }}</h2>
      <div class="card-tag">{{ disciplName }}</div>
    </div>

    <div class="card-main">
      <div class="card-details">
        <div class="detail-group">
          <div class="detail-item">
            <span class="detail-label">Дата регистрации:</span>
            <span class="detail-value">{{
              formatDateRange(dataregStart, dataregEnd)
            }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Дата участия:</span>
            <span class="detail-value highlight">{{
              formatDateRange(dataStart, dataEnd)
            }}</span>
          </div>
        </div>

        <div class="detail-group">
          <div class="detail-item">
            <span class="detail-label">Формат проведения:</span>
            <span class="detail-value">{{ typeComp }}</span>
          </div>
          <div class="detail-item">
            <span class="detail-label">Формат участия:</span>
            <span class="detail-value">{{ typeCommand }}</span>
          </div>
        </div>
      </div>

      <button class="toggle-btn" @click="toggle">
        {{ infoStatus }}
      </button>
    </div>

    <transition name="expand">
      <div v-if="allInfo" class="card-expanded-content">
        <slot name="expanded">
          <CardInfoComp :id="id" :typeCommand="typeCommand" />
        </slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import formatDateRange from "@/use/useFilterData";
import { computed, ref } from "vue";
import CardInfoComp from "./CardInfoComp.vue";

const props = defineProps({
  name: String,
  typeComp: String,
  typeCommand: String,
  status: String,
  dataregStart: String,
  dataregEnd: String,
  dataStart: String,
  dataEnd: String,
  disciplName: String,
  id: Number,
});

const allInfo = ref(false);
const infoStatus = computed(() => (allInfo.value ? "Скрыть" : "Подробнее"));

const toggle = () => {
  allInfo.value = !allInfo.value;
};
</script>

<style scoped>
.competition-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  padding: 20px;
  transition: all 0.3s ease;
  margin: 20px auto;
  max-width: 900px;
  overflow: hidden;
  border: 2px solid rgb(158, 158, 158);
}

.competition-card:hover {
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.12);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
  width: 100%;
}

.card-title {
  margin: 0;
  font-size: 2.05rem;
  font-weight: 700;
  color: #2c3e50;
}

.card-tag {
  background: var(--sin);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.card-main {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
}

.card-details {
  display: flex;
  gap: 40px;
}

.detail-group {
  display: flex;
  flex-direction: column;
  gap: 70px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-label {
  font-size: 0.85rem;
  color: #7f8c8d;
  font-weight: 600;
}

.detail-value {
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 500;
}

.highlight {
  color: #e74c3c;
  font-weight: 600;
}

.toggle-btn {
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
.toggle-btn .sin {
  background-color: var(--sin);
}
.toggle-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

.card-expanded-content {
  padding-top: 20px;
  margin-top: 20px;
  border-top: 1px solid #eee;
}

/* Анимации */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  max-height: 500px;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
  margin-top: 0;
  padding-top: 0;
}

/* Адаптация для мобильных */
@media (max-width: 768px) {
  .competition-card {
    padding: 15px;
    margin: 15px 0;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  .card-main {
    flex-direction: column;
    align-items: flex-start;
    gap: 20px;
  }

  .card-details {
    flex-direction: column;
    gap: 15px;
    width: 100%;
  }

  .toggle-btn {
    width: 100%;
  }
}
</style>

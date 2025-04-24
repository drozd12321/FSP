<template>
  <div v-if="act"><AppMsg :act="act" /></div>
  <div class="team-container">
    <div v-if="loading" class="loader-overlay"><Loader /></div>
    <div class="team-header">
      <h2 class="team-title">{{ nameCom }}</h2>
      <div class="team-meta">
        <span
          class="team-status"
          :class="status === 'finished' ? 'noactive' : 'active'"
          >{{ status === "finished" ? "Не активна" : "Активна" }}</span
        >
        <button class="toggle-btn" @click="toggleMembers">
          {{ showMembers ? "Скрыть участников" : "Показать участников" }}
        </button>
      </div>
    </div>

    <div class="team-info">
      <div class="info-card">
        <div class="info-label">Название соревнования</div>
        <div class="info-value">{{ nameCompet }}</div>
      </div>
      <div class="info-card">
        <div class="info-label">Дисциплина</div>
        <div class="info-value">{{ disciplineName }}</div>
      </div>
    </div>

    <transition name="slide">
      <div class="team-members" v-if="showMembers">
        <div class="cap">
          <h3 class="section-title">Участники команды</h3>
          <button
            v-if="isAdmin && status != 'finished' && !registr"
            class="btn danger"
            @click="sentZ"
          >
            Подать заявку
          </button>
          <button
            v-if="isAdmin && status != 'finished' && !registr"
            class="btn primary"
            @click="addteamid"
          >
            Пригласить в команду
          </button>
        </div>
        <div class="members-list">
          <div class="member-card" v-for="member in members" :key="member.id">
            <div class="member-avatar">
              <img src="/src/assets/user.png" />
            </div>
            <div class="member-info">
              <div class="member-name">{{ member.nickName }}</div>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { storeToRefs } from "pinia";
import { useMsgStore } from "@/stores/useMessageStore";
import AppMsg from "../message/AppMsg.vue";
import Loader from "../Loader.vue";
import { competitionStore } from "@/stores/storeComp";
const { getMsg } = storeToRefs(useMsgStore());
const compStore = competitionStore();
const msgStore = useMsgStore();
const showModal = ref(false);
const emit = defineEmits(["sentZavka", "modal"]);
const props = defineProps({
  nameCompet: String,
  status: String,
  disciplineName: String,
  nameCom: String,
  members: String,
  id: Number,
  registr: Boolean,
  teamComp: Number,
  teamId: Number,
});
const sentZ = () => {
  emit("sentZavka", { competition: props.teamComp, team_id: props.teamId });
};
const addteamid = () => {
  compStore.setteamId(props.teamId);
  emit("modal");
};
const loading = ref(false);
const showMembers = ref(false);
const isAdmin = ref();
const token = ref();
const toggleMembers = () => {
  showMembers.value = !showMembers.value;
};
const act = computed(() => {
  return getMsg.value;
});

const admin = () => {
  try {
    const userData = localStorage.getItem("user");
    if (!userData) return false;

    const idUs = JSON.parse(userData);
    if (!idUs?.id) return false;
    console.log(idUs.id);
    return String(idUs.id) === String(props.id);
  } catch (error) {
    console.error("Error checking admin status:", error);
    return false;
  }
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken");
  isAdmin.value = admin();
});
</script>

<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 100;
}
.team-container {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
  padding: 24px;
  max-width: 800px;
  margin: 10px auto;
}
.cap {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.team-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding-bottom: 16px;
  border-bottom: 1px solid #e2e8f0;
}

.team-title {
  color: #1e3a8a;
  font-size: 1.5rem;
  margin: 0;
}

.team-meta {
  display: flex;
  gap: 16px;
}

.team-status {
  background: #dcfce7;
  color: #166534;
  padding: 4px 8px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.team-status.noactive {
  background: #fee2e2; /* светло-красный фон */
  color: #991b1b;
}
.team-status.active {
  background: #dcfce7; /* светло-зеленый фон */
  color: #166534; /* темно-зеленый текст */
}

.team-id {
  color: #64748b;
  font-size: 0.875rem;
}

.team-info {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.info-card {
  background: #f8fafc;
  border-radius: 8px;
  padding: 12px 16px;
}

.info-label {
  color: #64748b;
  font-size: 0.75rem;
  margin-bottom: 4px;
}

.info-value {
  color: #1e293b;
  font-weight: 500;
}

.team-members {
  margin-bottom: 24px;
}

.section-title {
  color: #1e3a8a;
  font-size: 1.125rem;
  margin-bottom: 16px;
}

.members-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.member-card {
  display: flex;
  align-items: center;
  padding: 12px;
  background: #f8fafc;
  border-radius: 8px;
  gap: 12px;
}

.member-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  overflow: hidden;
}

.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-info {
  flex: 1;
}

.member-name {
  color: #1e293b;
  font-weight: 500;
}

.member-role {
  color: #64748b;
  font-size: 0.75rem;
}

.member-status {
  font-size: 0.75rem;
  font-weight: 600;
  padding: 4px 8px;
  border-radius: 20px;
}

.member-status.active {
  background: #dcfce7;
  color: #166534;
}

.member-status.pending {
  background: #fef9c3;
  color: #854d0e;
}

.member-status.inactive {
  background: #fee2e2;
  color: #991b1b;
}

.team-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.btn {
  padding: 8px 16px;
  border-radius: 6px;
  font-weight: 500;
  cursor: pointer;
  border: none;
  transition: all 0.2s;
}

.btn.primary {
  background: #3b82f6;
  color: white;
}

.btn.primary:hover {
  background: #2563eb;
}

.btn.danger {
  background: #fee2e2;
  color: #ef4444;
}

.btn.danger:hover {
  background: #fecaca;
}
.toggle-btn {
  padding: 6px 12px;
  background-color: #3b82f6;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.875rem;
  transition: background-color 0.2s;
}

.toggle-btn:hover {
  background-color: #2563eb;
}

/* Анимация появления */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.slide-enter-from,
.slide-leave-to {
  max-height: 0;
  opacity: 0;
  margin-bottom: 0;
}

.slide-enter-to,
.slide-leave-from {
  max-height: 500px;
  opacity: 1;
  margin-bottom: 24px;
}
</style>

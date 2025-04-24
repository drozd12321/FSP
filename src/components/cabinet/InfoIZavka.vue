<template>
  <div v-if="loading" class="loader-overlay"><Loader /></div>
  <div v-else>
    <div v-if="msgE"><AppMsg :act="msgE" @close="close" /></div>
    <div class="teams-container">
      <div class="teams-header">
        <h2>Мои заявки</h2>
      </div>

      <div class="teams-list">
        <div v-if="loading" class="loader-container">
          <Loader />
        </div>
        <div v-if="isData" class="empty-state">
          <img src="/src/assets/user.png" alt="Нет команд" class="empty-icon" />
          <p>Вы пока не подавали заявок на участие в командах</p>
          <button class="primary-btn" @click="gotoComm">Найти команду</button>
        </div>
        <div v-else>
          <Izavka
            v-for="zavka in izavka"
            :status="zavka.status_display"
            :description="zavka.text"
            :teamName="zavka.team.name"
            :competitionName="zavka.team.competition.name"
            :discipline_name="zavka.team.competition.discipline"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useMsgStore } from "@/stores/useMessageStore";
import { storeToRefs } from "pinia";
import InfoZavka from "./InfoZavka.vue";
import Loader from "../Loader.vue";
import AppMsg from "../message/AppMsg.vue";
import Izavka from "./Izavka.vue";
const router = useRouter();
const izavka = ref();
const msgStore = useMsgStore();
const { getMsg } = storeToRefs(useMsgStore());
const loading = ref(false);
const isData = ref(false);
const token = ref();
const getIzavka = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/user/vacancy-responses/",
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    console.log(response);
    isData.value = false;
    izavka.value = response.data.responses;
    loading.value = false;
    console.log("zavka", izavka.value);
    return response.data;
  } catch (error) {
    isData.value = true;
    loading.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const gotoComm = () => {
  router.push("/command");
};
const msgE = computed(() => {
  return getMsg.value;
});
const msg = ref({
  show: false,
  type: "",
  title: "",
});
const close = () => {
  msg.value = { show: false, type: "", title: "" };
};

onMounted(() => {
  token.value = localStorage.getItem("jwtToken").trim();
  getIzavka();
});
</script>

<style scoped>
.teams-container {
  margin-top: 20px;
  max-width: 1500px;
  padding: 2rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.teams-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid #9b9b9b;
}

.teams-header h2 {
  color: #e74c3c;
  font-size: 1.8rem;
  margin: 0;
}

.create-team-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.create-team-btn:hover {
  background-color: #2563eb;
}

.loader-container {
  display: flex;
  justify-content: center;
  padding: 2rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 0;
}

.empty-icon {
  width: 120px;
  height: 120px;
  margin-bottom: 1rem;
  opacity: 0.6;
}

.empty-state p {
  color: #666;
  margin-bottom: 1.5rem;
}

.primary-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
}

.primary-btn:hover {
  background-color: #2563eb;
}

.team-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.team-card {
  display: flex;
  border: 1px solid #eaeaea;
  border-radius: 8px;
  padding: 1.25rem;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.team-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
  border-color: #3b82f6;
}

.team-avatar {
  width: 60px;
  height: 60px;
  min-width: 60px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 1rem;
  background-color: #f0f0f0;
}

.team-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.team-info {
  flex-grow: 1;
}

.team-name {
  color: #333;
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.team-description {
  color: #666;
  font-size: 0.9rem;
  margin: 0 0 0.75rem 0;
  line-height: 1.4;
}

.team-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.85rem;
}

.team-type {
  padding: 0.25rem 0.5rem;
  border-radius: 4px;
  font-weight: 500;
}

.team-type.public {
  background-color: #e6f7ff;
  color: #1890ff;
}
.team-container {
  border: 2px solid #e74c3c;
}
.team-type.private {
  background-color: #fff2e8;
  color: #fa8c16;
}

.team-members {
  color: #666;
}

.team-actions {
  position: absolute;
  top: 0.5rem;
  right: 0.5rem;
}

.action-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #666;
  padding: 0.25rem;
  border-radius: 4px;
  transition: all 0.2s;
}

.action-btn:hover {
  color: #3b82f6;
  background-color: rgba(59, 130, 246, 0.1);
}

@media (max-width: 768px) {
  .teams-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 1rem;
  }

  .create-team-btn {
    width: 100%;
  }

  .team-cards {
    grid-template-columns: 1fr;
  }
}
</style>

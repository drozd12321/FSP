<template>
  <div v-if="act"><AppMsg :act="act" /></div>
  <div v-if="loading" class="loader-container">
    <Loader />
  </div>
  <div v-else class="container">
    <div class="teams-container">
      <div class="teams-header">
        <h2>Заявки команд</h2>
      </div>
      <div class="teams-list">
        <div v-if="isDataTeam" class="empty-state">
          <img src="/src/assets/user.png" alt="Нет команд" class="empty-icon" />
          <p>Команды пока не подали заявки на участия в соревнованиях</p>
        </div>
        <div v-else>
          <InfoZavka
            v-for="team in zavkateams"
            :isIndividual="true"
            :teamName="team.competition_name"
            :name="team.team_name"
            :team_members="team.team_members"
            :teamId="team.id"
            @open="openTeam"
          />
        </div>
      </div>
    </div>
    <div class="teams-container">
      <div class="teams-header">
        <h2>Заявки пользователей</h2>
      </div>
      <div class="teams-list">
        <div v-if="loading" class="loader-container">
          <Loader />
        </div>
        <div v-if="!isDataUser" class="empty-state">
          <img src="/src/assets/user.png" alt="Нет команд" class="empty-icon" />
          <p>Пользователи пока не подали заявки на участия в соревнованиях</p>
        </div>
        <div v-else>
          <InfoZavka
            v-for="user in zavkauser"
            :isIndividual="false"
            :name="user.user_info.nickName"
            :teamName="user.competition_name"
            :user="user.user_info"
            :userId="user.id"
            @close="openUser"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { useMsgStore } from "@/stores/useMessageStore";
import { storeToRefs } from "pinia";
const msgStore = useMsgStore();
const { getMsg } = storeToRefs(useMsgStore());
import Loader from "../Loader.vue";
import InfoZavka from "./InfoZavka.vue";
import AppMsg from "../message/AppMsg.vue";

const zavkateams = ref();
const zavkauser = ref();
const isDataTeam = ref(false);
const isDataUser = ref(false);
const loading = ref(false);
const token = ref();
const act = computed(() => {
  return getMsg.value;
});
const openTeam = async (action) => {
  try {
    loading.value = true;
    console.log(action);
    const response = await axios.patch(
      `http://10.8.0.23:8000/team-applications/${action.id}/response/`,
      {
        action: action.action,
        reason: action.reason,
      },
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    getZavka();
    if (action.action === "accept") {
      msgStore.setMesg({
        show: true,
        type: "succses",
        title: "Вы успешно подтвердили заявку",
      });
    } else {
      msgStore.setMesg({
        show: true,
        type: "succses",
        title: "Вы успешно отклонили заявку",
      });
    }
    loading.value = false;
    console.log(response.data);
  } catch (error) {
    loading.value = false;
    console.log(error);
  }
};
const openUser = async (action) => {
  try {
    loading.value = true;
    const response = await axios.patch(
      `http://10.8.0.23:8000/user-applications/${action.id}/response/`,
      {
        action: action.action,
        reason: action.reason,
      },
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    getZavkaUsers();
    console.log("action", action);
    if (action.action === "accept") {
      msgStore.setMesg({
        show: true,
        type: "succses",
        title: "Вы успешно подтвердили заявку",
      });
    } else {
      msgStore.setMesg({
        show: true,
        type: "succses",
        title: "Вы успешно отклонили заявку",
      });
    }
    loading.value = false;
    console.log(response.data);
  } catch (error) {
    loading.value = false;
    console.log(error);
  }
};
const getZavka = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/organizer/team/applications/",
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    zavkateams.value = response.data;
    loading.value = false;
    if (zavkateams.value.length === 0) {
      isDataTeam.value = true;
    } else {
      isDataTeam.value = false;
    }
    console.log("teams", zavkateams.value);
    return response.data;
  } catch (error) {
    isDataTeam.value = true;
    loading.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const getZavkaUsers = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/organizer/user/applications/",
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    zavkauser.value = response.data;
    loading.value = false;
    if (zavkauser.value.length === 0) {
      isDataUser.value = false;
    } else {
      isDataUser.value = true;
    }
    console.log("user", zavkauser.value);
    return response.data;
  } catch (error) {
    loading.value = false;
    isDataUser.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken").trim();
  getZavka();
  getZavkaUsers();
});
</script>

<style scoped>
.container {
  display: grid;
  grid-template-columns: repeat(2, 0.7fr);
  margin-left: 60px;
}
.teams-container {
  margin-top: 20px;
  max-width: 1500px;
  padding: 2rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-right: 80px;
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

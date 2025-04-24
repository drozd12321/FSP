<template>
  <div v-if="loading" class="loader-overlay"><Loader /></div>
  <div v-else>
    <div class="teams-container">
      <div class="teams-header">
        <div>
          <h2>Мои соревнования</h2>
        </div>
      </div>
      <AddCompetition />
      <div class="teams-list">
        <div v-if="loading" class="loader-container">
          <Loader />
        </div>
        <div v-if="isData" class="empty-state">
          <img src="/src/assets/user.png" alt="Нет команд" class="empty-icon" />
          <p>Вы пока не учавствовали в соревнованиях</p>
          <button class="primary-btn" @click="gotoComp">Учавствовать</button>
        </div>
        <div v-else class="teams-list">
          <Competitions
            v-for="comp in commpet.history"
            :name="comp.competition.name"
            :disciplineName="comp.competition.discipline"
            :status="comp.competition.status"
            :type="comp.competition.type"
            :res="comp.result"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { onMounted, ref } from "vue";
import Competitions from "./Competitions.vue";
import { useRouter } from "vue-router";
import Loader from "../Loader.vue";
import AddCompetition from "../compititions/AddCompetition.vue";
const router = useRouter();
const commpet = ref({
  stats: null,
  history: null,
});

const loading = ref(false);
const isData = ref(false);
const token = ref();
const role = ref();
const organized = ref();
const getCompetitions = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/competitions/history/",
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );

    commpet.value.stats = response.data.stats;
    commpet.value.history = response.data.history;
    if (commpet.value.history.length === 0) {
      isData.value = true;
    } else {
      isData.value = false;
    }
    console.log(commpet.value);
    loading.value = false;
    return response.data;
  } catch (error) {
    loading.value = false;
    isData.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const getCompetitionsOrganized = async () => {
  try {
    loading.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/competitions/organized/",
      {
        headers: {
          Authorization: `Token ${token.value}`,
          "Content-Type": "application/json",
        },
      }
    );
    isData.value = true;
    organized.value = response.data;
    console.log("org", organized.value);
    loading.value = false;
    return response.data;
  } catch (error) {
    loading.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const gotoComp = () => {
  router.push("/competitions");
};
onMounted(() => {
  token.value = localStorage.getItem("jwtToken").trim();
  role.value = localStorage.getItem("role").trim();

  getCompetitions();
  getCompetitionsOrganized();
});
</script>

<style scoped>
.stats {
  display: grid;
  grid-template-areas: "one two five", "three foo";
}
.one {
  grid-area: one;
}
.two {
  grid-area: two;
}
.five {
  grid-area: five;
}
.three {
  grid-area: three;
}
.one {
  grid-area: one;
}
.teams-list {
  display: flex;
  justify-content: space-around;
  width: 100%;
  gap: 20px;
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

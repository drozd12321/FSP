<template>
  <div class="teams-container">
    <div class="teams-header">
      <h2>Мои команды</h2>
      <button class="create-team-btn" @click="openCreateModal">
        + Создать команду
      </button>
    </div>

    <div class="teams-list">
      <div v-if="loading" class="loader-container">
        <Loader />
      </div>

      <!-- <div v-else-if="teams.length === 0" class="empty-state">
        <img src="@/assets/no-teams.svg" alt="Нет команд" class="empty-icon" />
        <p>У вас пока нет команд</p>
        <button class="primary-btn" @click="openCreateModal">
          Создать первую команду
        </button>
      </div> -->

      <div v-else class="team-cards">
        <div
          v-for="team in teams"
          :key="team.id"
          class="team-card"
          @click="openTeamDetails(team.id)"
        >
          <div class="team-avatar">
            <img :src="team.avatar || defaultTeamAvatar" alt="Аватар команды" />
          </div>
          <div class="team-info">
            <h3 class="team-name">{{ team.name }}</h3>
            <p class="team-description">
              {{ truncateDescription(team.description) }}
            </p>
            <div class="team-meta">
              <span
                class="team-type"
                :class="{ public: !team.is_private, private: team.is_private }"
              >
                {{ team.is_private ? "Приватная" : "Публичная" }}
              </span>
              <span class="team-members">
                👥 {{ team.members_count }}/{{ team.max_members }}
              </span>
            </div>
          </div>
          <div class="team-actions">
            <button class="action-btn" @click.stop="editTeam(team)">
              <i class="edit-icon">✏️</i>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Модальное окно создания команды -->
    <CreateTeamModal
      v-if="showCreateModal"
      @close="closeCreateModal"
      @created="handleTeamCreated"
    />
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const teams = ref([
  {
    id: 1,
    name: "Технологические лидеры",
    description: "Команда для разработки инновационных проектов в сфере IT",
    is_private: false,
    members_count: 5,
    max_members: 10,
    avatar: null,
  },
  {
    id: 2,
    name: "Тайные исследователи",
    description: "Закрытая группа для проведения научных экспериментов",
    is_private: true,
    members_count: 3,
    max_members: 5,
    avatar: null,
  },
]);

const loading = ref(false);
const showCreateModal = ref(false);

const truncateDescription = (text, length = 60) => {
  if (!text) return "";
  return text.length > length ? text.substring(0, length) + "..." : text;
};

const openCreateModal = () => {
  showCreateModal.value = true;
};

const closeCreateModal = () => {
  showCreateModal.value = false;
};

const handleTeamCreated = (newTeam) => {
  teams.value.unshift(newTeam);
  closeCreateModal();
};

const openTeamDetails = (teamId) => {
  console.log("Открываем детали команды", teamId);
  ды;
};

const editTeam = (team) => {
  console.log("Редактируем команду", team);
};

onMounted(() => {
  loading.value = true;
  setTimeout(() => {
    loading.value = false;
  }, 800);
});
</script>

<style scoped>
.teams-container {
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
  border-bottom: 1px solid #eaeaea;
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

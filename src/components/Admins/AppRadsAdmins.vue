<template>
  <div class="member-card">
    <div class="member-avatar" :style="avatarStyle">
      {{ userInitials }}
    </div>

    <div class="member-info">
      <div class="fio">
        <span class="member-name">{{ name }}</span>
        <span class="member-name">{{ surname }}</span>
        <span class="member-name">{{ patronymic }}</span>
      </div>
      <div class="member-stats">
        <div class="stat-item">
          <span class="stat-label">Email:</span>
          <span class="stat-value">{{ email }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Регион:</span>
          <span class="stat-value rating">{{ regionName }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  name: String,
  surname: String,
  patronymic: String,
  email: String,
  regionName: String,
});
</script>

<style scoped>
.fio {
  display: flex;
  gap: 5px;
  align-items: center;
}
.info {
  display: flex;
  width: 100%;
  justify-content: space-between;
}
.member-card {
  display: flex;
  background: white;
  border-radius: 12px;
  border: 1px solid #e0e0e0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  padding: 20px;
  transition: transform 0.3s ease;
  max-width: 1500px;
  margin: 50px auto;
}

.member-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.member-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: bold;
  margin-right: 20px;
  flex-shrink: 0;
  background: #3498db;
  color: white;
}

.member-info {
  flex-grow: 1;
  display: flex;
  justify-content: space-around;
  gap: 120px;
}

.member-name {
  margin: 0 0 5px 0;
  color: #2c3e50;
  font-size: 1.2rem;
}

.member-role {
  margin: 0 0 10px 0;
  color: #7f8c8d;
  font-size: 0.9rem;
}

.member-stats {
  display: flex;
  justify-content: space-between;
  gap: 115px;
}

.stat-item {
  display: flex;
  align-items: center;
}

.stat-label {
  color: #7f8c8d;
  margin-right: 5px;
  font-size: 0.9rem;
}

.stat-value {
  color: #2c3e50;
  font-weight: 600;
}

.rating {
  color: #e74c3c; /* Красный */
}

.member-actions {
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 8px;
  margin-left: 15px;
}

.action-btn {
  padding: 8px 12px;
  border-radius: 6px;
  font-size: 0.9rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  gap: 5px;
  border: none;
}

.message-btn {
  background: #3498db; /* Синий */
  color: white;
}

.message-btn:hover {
  background: #2980b9;
}

.profile-btn {
  background: white;
  color: #e74c3c; /* Красный */
  border: 1px solid #e74c3c;
}

.profile-btn:hover {
  background: #fdeaea;
}

.icon-message,
.icon-profile {
  font-size: 1rem;
}

@media (max-width: 600px) {
  .member-card {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }

  .member-avatar {
    margin-right: 0;
    margin-bottom: 15px;
  }

  .member-stats {
    justify-content: center;
  }

  .member-actions {
    flex-direction: row;
    margin-left: 0;
    margin-top: 15px;
  }
}
</style>

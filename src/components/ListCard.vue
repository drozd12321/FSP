<template>
  <div class="ultra-wide-card">
    <div class="wide-card-header">
      <h3 class="wide-card-title">Hackathon Pro 2024</h3>
      <span class="wide-card-tag">Хакатон</span>
    </div>

    <div class="wide-card-content">
      <div class="wide-card-details">
        <div class="wide-detail">
          <span class="wide-label">Дата:</span>
          <span class="wide-value">15-17 ноя</span>
        </div>
        <div class="wide-detail">
          <span class="wide-label">Формат:</span>
          <span class="wide-value">Онлайн</span>
        </div>
      </div>

      <button class="wide-card-btn">Участвовать</button>
    </div>
  </div>
</template>

<script setup>
// Логика карточки может быть добавлена здесь
</script>

<style scoped>
.ultra-wide-card {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 10px;
  box-shadow: 0 3px 15px rgba(0, 0, 0, 0.08);
  height: 100px;
  min-width: 800px;
  max-width: 1300px;
  padding: 15px 25px;
  font-family: "Segoe UI", Roboto, sans-serif;
  transition: transform 0.2s ease;
  margin-top: 20px;
}

.ultra-wide-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 5px 20px rgba(0, 0, 0, 0.12);
}

.wide-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.wide-card-title {
  margin: 0;
  font-size: 1.4rem;
  font-weight: 700;
  color: #2c3e50;
}

.wide-card-tag {
  background: var(--sin);
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
}

.wide-card-content {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-grow: 1;
}

.wide-card-details {
  display: flex;
  gap: 30px;
}

.wide-detail {
  display: flex;
  flex-direction: column;
}

.wide-label {
  font-size: 0.8rem;
  color: #7f8c8d;
  font-weight: 600;
  margin-bottom: 3px;
}

.wide-value {
  font-size: 1rem;
  color: #2c3e50;
  font-weight: 500;
}

.wide-card-btn {
  background: #e74c3c;
  color: white;
  border: none;
  padding: 8px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  height: 36px;
  min-width: 120px;
}

.wide-card-btn:hover {
  background: #c0392b;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .ultra-wide-card {
    min-width: 100%;
    height: 160px;
    padding: 12px 20px;
  }

  .wide-card-title {
    font-size: 1.2rem;
  }

  .wide-card-details {
    gap: 15px;
  }
}
</style>

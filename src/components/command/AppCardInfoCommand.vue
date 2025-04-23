<template>
  <div>
    <div class="competition-card-wide">
      <div class="card-image">
        <div class="image-placeholder"></div>
      </div>
      <div class="card-content-wide">
        <div class="card-header-wide">
          <h2 class="card-title-wide">{{ nameCommand }}</h2>
          <div class="card-tag-wide">5 участников</div>
        </div>

        <div class="card-details-wide">
          <div class="detail-column">
            <div class="detail-item">
              <span class="detail-label">Капитан:</span>
              <span class="detail-value">{{ captain }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Даты соревнования:</span>
              <span class="detail-value highlight">{{
                formatDateRange(startData, endData)
              }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Соревнование</span>
              <span class="detail-value highlight">{{ nameCompitition }}</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Создана:</span>
              <span class="detail-value highlight">{{
                formatRegDate(registrationStart)
              }}</span>
            </div>
          </div>
        </div>

        <div class="card-description-wide">
          <p>
            {{ description }}
          </p>
        </div>

        <div class="card-footer-wide">
          <button class="register-btn-wide">Присоединиться</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import formatDateRange from "@/use/useFilterData";
import formatRegDate from "@/use/useFilterRegData";
const props = defineProps({
  nameCommand: String,
  nameCompitition: String,
  description: String,
  captain: String,
  maxMembers: String,
  curentMembers: String,
  startData: String,
  endData: String,
  registrationStart: String,
});
</script>
<style scoped>
.competition-card-wide {
  display: flex;
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  max-width: 1400px;
  max-height: 300px;
  margin: 10px auto;
  font-family: "Segoe UI", Roboto, sans-serif;
}

.competition-card-wide:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.card-image {
  flex: 0 0 200px;
  background: #f5f5f5;
}

.image-placeholder {
  width: 70%;
  height: 100%;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  opacity: 0.8;
}

.card-content-wide {
  flex: 1;
  padding: 15px;
  display: flex;
  flex-direction: column;
}

.card-header-wide {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin: 10px 10px;
}

.card-title-wide {
  margin: 0;
  font-size: 1.6rem;
  font-weight: 600;
  color: #2c3e50;
}

.card-tag-wide {
  background: #e74c3c;
  color: white;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.card-details-wide {
  display: flex;
  gap: 30px;
  margin-bottom: 20px;
}

.detail-column {
  flex: 1;
  display: flex;
  justify-content: space-between;
  margin: auto 10px;
}

.detail-item {
  margin-bottom: 12px;
}

.detail-label {
  display: block;
  font-weight: 600;
  color: #7f8c8d;
  font-size: 0.9rem;
  margin-bottom: 3px;
}

.detail-value {
  display: block;
  color: #2c3e50;
  font-size: 1rem;
}

.highlight {
  color: #3498db;
  font-weight: 600;
}

.card-description-wide p {
  margin: 0 0 20px 0;
  color: #34495e;
  line-height: 1;
  font-size: 1rem;
  margin: 10px 10px;
}

.card-footer-wide {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.register-btn-wide {
  background: #3498db;
  color: white;
  border: none;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  font-size: 1rem;
}

.register-btn-wide:hover {
  background: #2980b9;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(52, 152, 219, 0.3);
}

.details-btn-wide {
  background: white;
  color: #3498db;
  border: 2px solid #3498db;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  font-size: 1rem;
}

.details-btn-wide:hover {
  background: #f0f8ff;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .competition-card-wide {
    flex-direction: column;
    max-width: 500px;
  }

  .card-image {
    flex: 0 0 150px;
  }

  .card-details-wide {
    flex-direction: column;
    gap: 0;
  }
}
</style>

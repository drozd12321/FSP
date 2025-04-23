<template>
  <div>
    <div class="competition-card-wide">
      <div class="card-image">
        <div class="image-placeholder"></div>
      </div>
      <div class="card-content-wide">
        <div class="card-header-wide">
          <h2 class="card-title-wide">Hack the Future 2024</h2>
          <div class="card-tag-wide">Командный хакатон</div>
        </div>

        <div class="card-details-wide">
          <div class="detail-column">
            <div class="detail-item">
              <span class="detail-label">Тип:</span>
              <span class="detail-value">Онлайн-соревнование</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Дата:</span>
              <span class="detail-value highlight">15-17 ноября 2024</span>
            </div>
          </div>

          <div class="detail-column">
            <div class="detail-item">
              <span class="detail-label">Уровень:</span>
              <span class="detail-value">Профессиональный</span>
            </div>
            <div class="detail-item">
              <span class="detail-label">Призы:</span>
              <span class="detail-value">$10,000</span>
            </div>
          </div>
        </div>

        <div class="card-description-wide">
          <p>
            48-часовое соревнование по разработке инновационных решений в
            области искусственного интеллекта и анализа данных. Участвуйте в
            составе команды до 5 человек.
          </p>
        </div>

        <div class="card-footer-wide">
          <button class="register-btn-wide" @click="createCommand">
            {{
              typeCommand === "Командное"
                ? "Зарегестрировать команду"
                : "Зарегестрироваться"
            }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useCommandStore } from "@/stores/storeCommand";
const comStore = useCommandStore();
const props = defineProps({
  id: Number,
  typeCommand: String,
});
const createCommand = () => {
  comStore.setCreating(true);
  comStore.setId(props.id);
  comStore.setType(props.typeCommand);
};
</script>
<style scoped>
.competition-card-wide {
  display: flex;
  background: white;
  border-radius: 12px;

  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  max-width: 900px;
  margin: 0 auto;
  font-family: "Segoe UI", Roboto, sans-serif;
}

.competition-card-wide:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
}

.card-image {
  flex: 0 0 250px;
  background: #f5f5f5;
}

.image-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #e74c3c, #c0392b);
  opacity: 0.8;
}

.card-content-wide {
  flex: 1;
  padding: 25px;
  display: flex;
  flex-direction: column;
}

.card-header-wide {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.card-title-wide {
  margin: 0;
  font-size: 1.8rem;
  font-weight: 700;
  color: #2c3e50;
}

.card-tag-wide {
  background: var(--sin);
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
  font-size: 1.05rem;
}

.highlight {
  color: #e74c3c;
  font-weight: 600;
}

.card-description-wide p {
  margin: 0 0 20px 0;
  color: #34495e;
  line-height: 1.6;
  font-size: 1rem;
}

.card-footer-wide {
  display: flex;
  gap: 15px;
  margin-top: auto;
}

.register-btn-wide {
  background: var(--sin);
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
  background: #c0392b;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(231, 76, 60, 0.3);
}

.details-btn-wide {
  background: white;
  color: #e74c3c;
  border: 2px solid #e74c3c;
  padding: 12px 25px;
  border-radius: 6px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  flex: 1;
  font-size: 1rem;
}

.details-btn-wide:hover {
  background: #f9f2f2;
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

<template>
  <div v-if="loading" class="loader-overlay"><Loader /></div>
  <div v-else class="profile-container">
    <div class="profile-header">
      <h2>Личный кабинет</h2>
      <div class="id">Уникальный номер: {{ user.info.user_id }}</div>
    </div>
    <div class="profile-content">
      <div class="avatar-section">
        <div class="avatar-wrapper">
          <img src="../../assets/user.png" alt="Аватар" class="avatar-image" />
          <button class="avatar-upload-btn" @click="triggerFileInput">
            <i class="upload-icon">↑</i> Сменить фото
          </button>
          <input
            type="file"
            ref="fileInput"
            @change="handleAvatarUpload"
            accept="image/*"
            style="display: none"
          />
        </div>
      </div>
      <div class="personal-data-section">
        <h3 class="section-title">Личные данные</h3>
        <form @submit.prevent="saveProfile" class="profile-form">
          <div class="fio">
            <div class="form-group">
              <label for="fullName">Фамилия</label>
              <input
                type="text"
                id="surname"
                v-model="user.info.surname"
                placeholder="Иванов"
              />
            </div>
            <div class="form-group">
              <label for="fullName">Имя</label>
              <input
                type="text"
                id="name"
                v-model="user.info.name"
                placeholder="Иван"
              />
            </div>
            <div class="form-group">
              <label for="fullName">Отчество</label>
              <input
                type="text"
                id="patronymic"
                v-model="user.info.patronymic"
                placeholder="Иванович"
              />
            </div>
          </div>

          <div class="form-group">
            <label for="email">Регион</label>
            <input
              type="text"
              id="region"
              v-model="user.info.region_name"
              placeholder="Новгородская область"
            />
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input
              type="email"
              id="email"
              v-model="user.user.email"
              placeholder="example@mail.com"
            />
          </div>
          <div class="form-group">
            <label for="email">Роль</label>
            <input
              type="text"
              id="role"
              v-model="user.info.role_name"
              disabled
              placeholder="example@mail.com"
            />
          </div>
          <div class="form-group">
            <label for="birthDate">Дата рождения</label>
            <input type="date" id="birthDate" v-model="user.info.birthday" />
          </div>
          <div class="form-actions">
            <button type="submit" class="save-btn">Сохранить изменения</button>
            <button type="button" class="cancel-btn" @click="resetForm">
              Отмена
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script setup>
import getUser from "@/use/useGetUser";
import { onMounted, ref, watch } from "vue";
import Loader from "../Loader.vue";
const props = defineProps({
  data: Object,
});
const user = ref({
  info: {
    name: "",
    surname: "",
    patronymic: "",
    email: "",
    birthDate: "",
    region: "",
    role: "",
  },
  user: {
    email: "",
  },
});
const fileInput = ref(null);
const triggerFileInput = () => {
  fileInput.value.click();
};
const handleAvatarUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      user.value.avatar = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};
const saveProfile = () => {
  alert("Данные успешно сохранены!");
};

const resetForm = () => {
  user.value = {
    info: {
      name: "",
      surname: "",
      patronymic: "",
      email: "",
      birthDate: "",
      region: "",
      role: "",
    },
    user: {
      email: "",
    },
  };
};

const token = ref("");
const loading = ref();
const userData = ref();
onMounted(async () => {
  try {
    loading.value = true;
    token.value = localStorage.getItem("jwtToken");
    if (!token.value) {
      throw new Error("Токен не найден");
    }
    user.value = await getUser(token.value);
    console.log(user);
  } catch (error) {
    console.error("Ошибка при загрузке пользователя:", error);
  } finally {
    loading.value = false;
  }
});
// onMounted(updateUserFromProps);
// watch(() => props.data, updateUserFromProps);
</script>

<style scoped>
.fio {
  display: flex;
  width: 100%;
  gap: 90px;
}
.id {
  margin-top: 10px;
}
.profile-container {
  max-width: 1700px;

  padding: 2rem;
  background: #ffffff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.profile-header {
  text-align: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid #eaeaea;
}

.profile-header h2 {
  color: #e74c3c;
  font-size: 1.8rem;
  margin: 0;
}

.profile-content {
  display: flex;
  gap: 2rem;
}

.avatar-section {
  flex: 1;
  display: flex;
  justify-content: center;
}

.avatar-wrapper {
  text-align: center;
}

.avatar-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #3b82f6;
  margin-bottom: 1rem;
}

.avatar-upload-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin: 0 auto;
}
.avatar-upload-btn:hover {
  background-color: #2563eb;
}
.upload-icon {
  font-size: 1rem;
}
.personal-data-section {
  flex: 2;
}
.section-title {
  color: #e74c3c;
  margin-top: 0;
  margin-bottom: 1.5rem;
  font-size: 1.3rem;
}
.profile-form {
  display: flex;
  flex-direction: column;
  gap: 1.2rem;
}
.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.form-group label {
  font-weight: 500;
  color: #555;
}
.form-group input {
  padding: 0.75rem;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 1rem;
  transition: border-color 0.3s;
}
.form-group input:focus {
  border: 1px solid var(--sin);
  outline: none;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}
.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 1rem;
}
.save-btn {
  background-color: #3b82f6;
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: background-color 0.3s;
  flex: 1;
}
.save-btn:hover {
  background-color: #2563eb;
}
.cancel-btn {
  background-color: #f8f9fa;
  color: #555;
  border: 1px solid #ddd;
  padding: 0.75rem 1.5rem;
  border-radius: 6px;
  cursor: pointer;
  font-size: 1rem;
  transition: all 0.3s;
  flex: 1;
}
.cancel-btn:hover {
  background-color: #e9ecef;
  border-color: #ced4da;
}
@media (max-width: 768px) {
  .profile-content {
    flex-direction: column;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>

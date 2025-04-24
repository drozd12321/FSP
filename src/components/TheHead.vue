<template>
  <header class="header-container">
    <div class="header-content logo">
      <img
        src="../assets/photo_2025-04-21_20-08-46.png"
        alt="Федерация спортивного программирования"
        class="logo-img"
      />
      <span class="logo-text"
        ><RouterLink class="nav-link h2" to="/">Федерация СП</RouterLink>
      </span>

      <nav class="head">
        <div class="nav-item">
          <RouterLink to="/competitions" class="nav-link"
            >Соревнования</RouterLink
          >
        </div>
        <div class="nav-item">
          <RouterLink to="/command" class="nav-link">Поиск команд</RouterLink>
        </div>
        <div class="nav-item">
          <RouterLink to="/rating" class="nav-link">Рейтинг</RouterLink>
        </div>
        <div class="nav-item">
          <RouterLink to="/admins" class="nav-link">Представители</RouterLink>
        </div>
        <div class="nav-item">
          <RouterLink to="/news" class="nav-link">Новости</RouterLink>
        </div>
        <div class="nav-item">
          <RouterLink to="/FAQ" class="nav-link">FAQ</RouterLink>
        </div>
      </nav>
      <div class="user-actions">
        <a
          href="https://t.me/FSPCompetitions_Bot"
          target="_blank"
          class="icon-link"
          title="Телеграммбот"
        >
          <img src="/src/assets/svg/i (2).png" />
        </a>
        <RouterLink to="/cabinet/message" class="icon-link" title="Сообщения">
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path
              d="M20 2H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h14l4 4V4c0-1.1-.9-2-2-2zm-2 12H6v-2h12v2zm0-3H6V9h12v2zm0-3H6V6h12v2z"
            />
          </svg>
        </RouterLink>

        <RouterLink
          :to="isAuth ? '/cabinet' : '/auth'"
          class="icon-link"
          title="Личный кабинет"
        >
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path
              d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"
            />
          </svg>
        </RouterLink>

        <button
          class="icon-link logout-btn"
          v-if="isAuth"
          @click="logout"
          title="Выйти"
        >
          <svg
            class="icon"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 24 24"
            fill="white"
          >
            <path
              d="M10.09 15.59L11.5 17l5-5-5-5-1.41 1.41L12.67 11H3v2h9.67l-2.58 2.59zM19 3H5c-1.11 0-2 .9-2 2v4h2V5h14v14H5v-4H3v4c0 1.1.89 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"
            />
          </svg>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useRouter } from "vue-router";

const { isAuth } = useAuthStore();
const authStore = useAuthStore();
const router = useRouter();
const logout = () => {
  authStore.removeToken();
  router.push("/auth");
};
</script>
<style scoped>
.header-container {
  background: rgb(34, 34, 34);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
}
img {
  margin-top: 10px;
  height: 40px;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 0 auto;
  padding: 0 20px;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  text-decoration: none;
  color: white;
  font-weight: 600;
  font-size: 20px;
  transition: transform 0.3s ease;
}

.logo-img {
  height: 40px;
  margin-right: 12px;
}

.logo-text {
  margin-top: 3px;
}

.head {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1;
}
a {
  list-style: none;
  text-decoration: none;
  color: white;
}
.nav-item {
  position: relative;
  padding: 0 15px;
  transition: all 0.3s ease;
}
.nav-link.h2 {
  font-size: 25px;
  font-weight: 600;
}
.nav-link {
  color: white;
  text-decoration: none;
  font-size: 16px;
  font-weight: 500;
  letter-spacing: 0.5px;
  padding: 8px 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  position: relative;
}

.nav-link:hover {
  background-color: rgba(255, 255, 255, 0.15);
}

.nav-link::after {
  content: "";
  position: absolute;
  bottom: -5px;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background-color: white;
  transition: width 0.3s ease;
}

.nav-link:hover::after {
  width: 70%;
}

.active {
  font-weight: 600;
  border-bottom: 2px solid white;
}

.router-link-active::after {
  width: 70%;
  background-color: white;
}

.user-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.icon-link {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  transition: all 0.3s ease;
  cursor: pointer;
}

.icon-link:hover {
  background-color: rgba(255, 255, 255, 0.2);
  transform: translateY(-2px);
}

.icon {
  width: 24px;
  height: 24px;
}

.badge {
  position: absolute;
  top: -5px;
  right: -5px;
  background-color: #ffeb3b;
  color: #333;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 10px;
  font-weight: bold;
}

.logout-btn {
  background: none;
  border: none;
  padding: 0;
}

@media (max-width: 1024px) {
  .header-content {
    padding: 0 15px;
  }

  .nav-item {
    padding: 0 10px;
  }

  .nav-link {
    font-size: 14px;
    padding: 6px 8px;
  }

  .user-actions {
    gap: 15px;
  }
}

@media (max-width: 768px) {
  .header-content {
    height: 60px;
    padding: 0 10px;
  }

  .logo-text {
    display: none;
  }

  .head {
    display: none; /* В мобильной версии можно использовать бургер-меню */
  }

  .user-actions {
    gap: 10px;
  }

  .icon-link {
    width: 32px;
    height: 32px;
  }

  .icon {
    width: 20px;
    height: 20px;
  }
}
</style>

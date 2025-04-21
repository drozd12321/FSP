import { ref, computed } from "vue";
import { defineStore } from "pinia";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("jwtToken"));
  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("jwtToken", newToken);
  }
  function removeToken() {
    token.value = null;
    localStorage.removeItem("jwtToken");
  }
  const getToken = computed(() => token.value);
  const isAuth = computed(() => !!token.value);
  async function login(username, password) {
    try {
      // Закомментированный запрос — пример того, как будет работать логин
      // const response = await fetch('https://api.example.com/login', {
      //   method: 'POST',
      //   headers: {
      //     'Content-Type': 'application/json',
      //   },
      //   body: JSON.stringify({ username, password }),
      // });

      // if (!response.ok) {
      //   throw new Error('Ошибка при авторизации');
      // }

      // const data = await response.json();

      // Для демонстрации, заменим это на setTimeout, чтобы имитировать асинхронную операцию
      setTimeout(() => {
        setToken("new-jwt-token");
        console.log(
          "User logged in successfully",
          localStorage.getItem("jwtToken")
        );
      }, 1000);

      return true;
    } catch (error) {
      console.error("Ошибка при логине:", error);
      return false; // Логин неудачен
    }
  }

  // Возвращаем состояние, методы и геттеры
  return { token, setToken, removeToken, getToken, isAuth, login };
});

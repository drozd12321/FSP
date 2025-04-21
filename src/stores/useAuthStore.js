import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

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
  async function login(url, formstate) {
    try {
      console.log("sdsds");
      console.log(formstate);
      const responce = await axios.post(url, formstate);
      console.log(responce.data);
      setToken(responce.data);
      return true;
    } catch (error) {
      console.error("Ошибка при логине:", error);
      return false; // Логин неудачен
    }
  }

  // Возвращаем состояние, методы и геттеры
  return { token, setToken, removeToken, getToken, isAuth, login };
});

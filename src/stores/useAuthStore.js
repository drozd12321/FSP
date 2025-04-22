import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("jwtToken"));
  const role = ref(localStorage.getItem("role"));
  const error = ref(null);
  const isLoading = ref(false);

  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("jwtToken", newToken);
    error.value = null;
  }
  function setRole(newRole) {
    role.value = newRole;
    localStorage.setItem("role");
    error.value = null;
  }
  function removeToken() {
    token.value = null;
    localStorage.removeItem("jwtToken");
  }
  function setError(err) {
    error.value = err;
  }
  const getError = computed(() => error.value);
  const getToken = computed(() => token.value);
  const isAuth = computed(() => !!token.value);
  async function login(url, formstate) {
    try {
      isLoading.value = true;
      console.log("gg");
      error.value = null;
      const response = await axios.post(url, formstate);
      if (!response.data?.token) {
        throw new Error("Сервер не вернул токен");
      }
      console.log(response);
      setToken(response.data.token);
      setRole(response.data.role);
      isLoading.value = false;

      console.log(isLoading);
      return true;
    } catch (err) {
      setError(err.response.data);
      console.log(err.response.data);
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  return {
    token,
    error,
    getError,
    isLoading,
    setToken,
    removeToken,
    getToken,
    isAuth,
    login,
    setError,
    setRole,
  };
});

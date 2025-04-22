import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("jwtToken"));
  const role = ref(localStorage.getItem("role"));
  const user = ref(localStorage.getItem("user"));
  const error = ref(null);
  const isLoading = ref(false);

  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("jwtToken", newToken);
    error.value = null;
  }
  function setUser(newUser) {
    user.value = newUser;
    localStorage.setItem("user", JSON.stringify(newUser));
  }
  function setRole(newRole) {
    role.value = newRole;
    localStorage.setItem("role", newRole);
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
  const getUser = computed(() => user.value);
  const getToken = computed(() => token.value);
  const isAuth = computed(() => !!token.value);
  async function login(url, formstate) {
    try {
      isLoading.value = true;
      error.value = null;
      const response = await axios.post(url, formstate);
      if (!response.data?.token) {
        throw new Error("Сервер не вернул токен");
      }
      const tk = response.data.token;
      const rl = response.data.role;
      console.log(rl.id);
      console.log(response.data.user);
      setToken(tk);
      setRole(rl.id);
      setUser(response.data.user);
      console.log("log1", response);

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
    setUser,
    getUser,
  };
});

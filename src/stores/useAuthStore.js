import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("jwtToken"));
  const role = ref(localStorage.getItem("role"));
  const user = ref(localStorage.getItem("user"));
  const error = ref(null);
  const msg = ref({
    show: false,
    type: "",
    title: "",
  });
  const isLoading = ref(false);

  function setToken(newToken) {
    token.value = newToken;
    localStorage.setItem("jwtToken", newToken);
    error.value = null;
  }
  function setMesg(newVal) {
    msg.value.show = newVal.show;
    msg.value.title = newVal.title;
    msg.value.type = newVal.type;
    console.log(msg.value);
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
  const getMsg = computed(() => msg.value);
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
      setToken(tk);
      setRole(rl.id);
      setUser(response.data.user);
      isLoading.value = false;
      return true;
    } catch (err) {
      setError(err.response.data);
      return false;
    } finally {
      isLoading.value = false;
    }
  }
  return {
    getMsg,
    setMesg,
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

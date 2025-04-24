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
    role.value = newRole.id;
    localStorage.setItem("role", newRole);
    error.value = null;
  }
  function removeToken() {
    token.value = null;
    localStorage.removeItem("jwtToken");
  }
  function setError(err) {
    error.value = err;
    console.log(err.value);
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

      // Проверка наличия данных в ответе
      if (!response?.data) {
        throw new Error("Сервер вернул пустой ответ");
      }

      // Валидация структуры ответа для регистрации/логина
      if (url.includes("/register/")) {
        if (!response.data.user || !response.data.token) {
          throw new Error("Ожидайте подтверждения регистраии");
        }
      } else {
        if (!response.data.token) {
          throw new Error("Не получен токен авторизации");
        }
      }
      setToken(response.data.token);
      setUser(response.data.user);
      if (response.data.role) {
        setRole(response.data.role.id);
      } else if (response.data.user?.role) {
        setRole(response.data.user.role.id || response.data.user.role);
      }
      setMesg({
        show: true,
        type: "succses",
        title: url.includes("/register/")
          ? "Вы успешно зарегистрировались"
          : "Вход выполнен успешно",
      });
      console.log(response.data.role.id);
      return true;
    } catch (err) {
      console.error("Auth error:", err);

      // Улучшенная обработка ошибок
      let errorMessage = "Произошла ошибка при авторизации";

      if (err.response) {
        // Сервер вернул ошибку
        errorMessage =
          err.response.data?.non_field_errors?.[0] ||
          err.response.data?.detail ||
          err.response.data?.message ||
          err.response.data?.email[0] ||
          err.response.data?.nickname[0] ||
          JSON.stringify(err.response.data);
      } else if (err.request) {
        errorMessage = "Сервер не отвечает";
      } else {
        // Ошибка настройки запроса
        errorMessage = err.message;
      }

      setMesg({
        show: true,
        type: "error",
        title: errorMessage,
      });

      setError(errorMessage);
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

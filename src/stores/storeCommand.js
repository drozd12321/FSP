import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./useAuthStore";

export const useCommandStore = defineStore("command", () => {
  const isCreating = ref(false);
  const type = ref();
  const loading = ref(false);
  const errorAddCommand = ref(null);
  const msg = ref({
    show: false,
    type: "",
    title: "",
  });
  const Id = ref();
  function setError(err) {
    errorAddCommand.value = err;
  }
  function setCreating(newVal) {
    isCreating.value = newVal;
  }
  function setMesg(newVal) {
    msg.value.show = newVal.show;
    msg.value.title = newVal.title;
    msg.value.type = newVal.type;
  }
  function setId(newId) {
    Id.value = newId;
  }
  function setType(newType) {
    type.value = newType;
  }
  async function addCommand(url, formstate, token) {
    try {
      loading.value = true;
      console.log("form", formstate, token);
      if (!token) {
        throw new Error("No authentication token available");
      }
      const response = await axios.post(url, formstate, {
        headers: {
          Authorization: `Token ${token}`,
          "Content-Type": "application/json",
        },
      });
      setMesg({
        show: true,
        title: "Вы успешно подали заявку",
        type: "succses",
      });
      console.log(msg);
      loading.value = false;
      setCreating(false);
      return true;
    } catch (err) {
      setMesg({
        show: true,
        title: "Вы уже подали одну заявку больше нельзя",
        type: "error",
      });
      console.log(msg);
      setError(err.response?.data || err.message);
      setCreating(false);
      console.log(isCreating);
      loading.value = false;
      return false;
    } finally {
      setCreating(false);
      loading.value = false;
    }
  }

  const getCreating = computed(() => isCreating.value);
  const getMsg = computed(() => msg.value);
  const getLoading = computed(() => loading.value);
  const getError = computed(() => errorAddCommand.value);
  const getId = computed(() => Id.value);
  const getType = computed(() => type.value);
  return {
    setMesg,
    getMsg,
    setError,
    getType,
    setType,
    setId,
    getId,
    getLoading,
    setCreating,
    getCreating,
    getError,
    addCommand,
  };
});

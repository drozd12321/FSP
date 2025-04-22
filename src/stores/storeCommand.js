import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./useAuthStore";

export const useCommandStore = defineStore("command", () => {
  const isCreating = ref(false);
  const loading = ref(false);
  const errorAddCommand = ref(null);
  const Id = ref();
  function setError(err) {
    errorAddCommand.value = err;
  }
  function setCreating(newVal) {
    isCreating.value = newVal;
    console.log(isCreating.value);
  }
  function setId(newId) {
    Id.value = newId;
  }
  async function addCommand(formstate, token) {
    try {
      loading.value = true;
      if (!token) {
        throw new Error("No authentication token available");
      }
      const response = await axios.post(
        "http://10.8.0.23:8000/teams/",
        formstate,
        {
          headers: {
            Authorization: `Token ${token}`,
            "Content-Type": "application/json",
          },
        }
      );

      console.log(response.data);
      loading.value = false;
      return true;
    } catch (err) {
      setError(err.response?.data || err.message);
      loading.value = false;
      return false;
    } finally {
      loading.value = false;
    }
  }

  const getCreating = computed(() => isCreating.value);
  const getLoading = computed(() => loading.value);
  const getError = computed(() => errorAddCommand.value);
  const getId = computed(() => Id.value);
  return {
    setError,
    setId,
    getId,
    getLoading,
    setCreating,
    getCreating,
    getError,
    addCommand,
  };
});

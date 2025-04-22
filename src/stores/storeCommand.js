import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const commandStore = defineStore("comp", () => {
  const isCreating = ref(false);
  const errorAddCommand = ref(null);
  function setError(err) {
    errorAddCommand.value = err;
  }
  function setCreating(newVal) {
    isCreating.value = newVal;
    console.log(isCreating.value);
  }
  const getCreating = computed(() => isCreating.value);
  const getError = computed(() => errorAddCommand.value);
  return {
    setError,
    setCreating,
    getCreating,
    getError,
  };
});

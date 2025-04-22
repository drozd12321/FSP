import { ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const competitionStore = defineStore("comp", () => {
  const token = ref(localStorage.getItem("jwtToken"));
  const errorAddCompetition = ref(null);
  const loading = ref(false);
  function setError(err) {
    errorAddCompetition.value = err;
  }
  async function addCompetitions(formstate) {
    try {
      loading.value = true;
      const response = await axios.post(
        "http://10.8.0.23:8000/competitions/create/",
        formstate
      );
      console.log(response.data);
      loading.value = false;
      return true;
    } catch (err) {
      setError(errorAddCompetition.response.data);
      loading.value = false;
      return false;
    } finally {
      loading.value = false;
    }
  }
  return {
    token,
    errorAddCompetition,
    loading,
    addCompetitions,
  };
});

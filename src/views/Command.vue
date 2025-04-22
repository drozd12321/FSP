<template>
  <div></div>
</template>
<script setup>
import AddCommand from "@/components/AddCommand.vue";
import axios from "axios";
import { onMounted } from "vue";
const getCommand = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/teams/public/");
    comp.value = response.data;
    console.log(comp.value);
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getCommand();
});
</script>
<style scoped></style>

<template>
  <div>
    <AppMsg v-if="act1?.show" :act="act1" />
    <h1>Федерация спортивного программирования</h1>
    <CardRussia />
  </div>
</template>
<script setup>
import AppMsg from "@/components/message/AppMsg.vue";
import { computed, onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
import axios from "axios";
import CardRussia from "@/components/home/CardRussia.vue";
const { getMsg } = storeToRefs(useAuthStore());
const act1 = computed(() => {
  return getMsg.value;
});
function getISODateTime() {
  return new Date().toISOString().replace(/\.\d{3}/, "");
}
const getDat = async () => {
  try {
    const isoDate = getISODateTime();
    console.log(isoDate);
    const response = await axios.post(
      "http://10.8.0.23:8000/competitions/status/",
      { time: isoDate }
    );

    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);

    throw error;
  }
};
onMounted(() => {
  getDat();
});
</script>
<style scoped>
h1 {
  color: #e74c3c;
  text-align: center;
}
</style>

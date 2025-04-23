<template>
  <div class="faq-container">
    <h1 class="faq-title">
      Представители Федерации по спортивному программированию
    </h1>
  </div>
  <div v-if="dataload" class="loader-overlay"><Loader /></div>
  <div v-else v-for="admin in admins" class="container">
    <AppRadsAdmins
      :name="admin.name"
      :surname="admin.surname"
      :patronymic="admin.patronymic"
      :email="admin.email"
      :regionName="admin.region_name"
    />
  </div>
</template>
<script setup>
import AppRadsAdmins from "@/components/Admins/AppRadsAdmins.vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
const admins = ref();
const dataload = ref(false);
const getAdmins = async () => {
  try {
    dataload.value = true;
    const response = await axios.get(
      "http://10.8.0.23:8000/regional-representatives/"
    );
    admins.value = response.data;
    console.log(admins.value);
    dataload.value = false;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    dataload.value = false;
    throw error;
  }
};
onMounted(() => {
  getAdmins();
});
</script>
<style scoped>
.faq-container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem 1rem;
  color: #ef4444;
  font-family: "Inter", -apple-system, BlinkMacSystemFont, sans-serif;
}
.loader-overlay {
  display: flex;
  justify-content: center;

  height: 400px;
}
</style>

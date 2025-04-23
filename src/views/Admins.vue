<template>
  <div v-for="admin in admins" class="container">
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
import TheHead from "@/components/TheHead.vue";
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
<style scoped></style>

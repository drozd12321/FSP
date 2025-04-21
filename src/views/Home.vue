<template>
  <TheHead />
  <button @click="logout">Выйти</button>
</template>
<script setup>
import TheHead from "@/components/TheHead.vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { useRouter } from "vue-router";
const authStore = useAuthStore();
const router = useRouter();
const logout = async () => {
  try {
    authStore.removeToken();
    console.log("logout");
    router.push("/auth");
  } catch (error) {
    console.log(error);
  }
};
</script>
<style scoped></style>

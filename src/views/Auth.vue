<template>
  <button @click="login">Войти</button>
</template>
<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useRouter } from "vue-router";
const authStore = useAuthStore();
const router = useRouter();
const login = async () => {
  try {
    await authStore.login("name", "passwd");
    console.log("login");
    router.push("/");
  } catch (error) {
    console.log(error);
  }
};
</script>
<style scoped></style>

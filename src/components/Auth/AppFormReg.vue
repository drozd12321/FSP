<template>
  <form class="form" @submit.prevent="login">
    <div class="inf">
      <h2>Регистрация</h2>
      <div class="inpdiv">
        <label class="label" for="email">Email:</label>
        <input />
      </div>
      <div class="inpdiv">
        <label class="label" for="email">Password:</label>
        <input />
      </div>
      <button type="submit">Войти</button>
    </div>
  </form>
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
<style scoped>
form {
  width: 100%;
}
.inf {
  width: 100%;
}
</style>

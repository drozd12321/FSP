<template>
  <form class="form" @submit.prevent="login">
    <div class="inf">
      <div class="pole" v-if="mode === 'log'">
        <DivLogin />
      </div>
      <div class="pole" v-if="mode === 'reg'">
        <DivReg />
      </div>
    </div>
  </form>
</template>
<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { useRouter } from "vue-router";
import DivReg from "./DivReg.vue";
import DivLogin from "./DivLogin.vue";
const props = defineProps({
  mode: String,
});
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
  width: 700px;
  height: 60vh;
}
.inf {
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.pole {
  height: auto;
  width: 550px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* равномерно распределяем элементы */
  padding: 20px;
  box-sizing: border-box;
  gap: 10px;
}
</style>

<template>
  <form class="form" @submit.prevent="login">
    <div class="inf">
      <transition name="fade" mode="out-in">
        <div class="pole" v-if="mode === 'log'">
          <DivLogin />
        </div>
        <div class="pole" v-else>
          <DivReg />
        </div>
      </transition>
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
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}
form {
  width: 700px;
}
.inf {
  height: 100%;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  align-items: center;
  transition: all 0.5s ease;
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

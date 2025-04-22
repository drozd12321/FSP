<template>
  <div class="error-overlay" v-if="getError">
    <AppErrorMsg />
  </div>
  <div v-if="isLoading" class="loader-overlay"><Loader /></div>
  <form class="form" @submit.prevent="login">
    <div class="inf">
      <transition name="fade" mode="out-in">
        <div class="pole" v-if="mode === 'log'">
          <DivLogin v-model:emailVal="email" v-model:passwordVal="password" />
          <button type="submit" :disabled="isSubmitting">
            <!-- Убрали @click -->
            {{ isLoad ? "Загрузка" : "Войти" }}
          </button>
        </div>
        <div class="pole" v-else>
          <DivReg
            v-model:emailVal="email"
            v-model:passwordVal="password"
            v-model:firstnameVal="firstname"
            v-model:lastnameVal="lastname"
            v-model:nameVal="name"
            v-model:nicknameVal="nickname"
            v-model:regionVal="region"
            v-model:statusVal="status"
            v-model:dtVal="dt"
          />
          <button type="submit" :disabled="isSubmitting">
            <!-- Убрали @click -->
            Зарегистрироваться
          </button>
        </div>
      </transition>
    </div>
  </form>
</template>
<script setup>
import DivReg from "./DivReg.vue";
import DivLogin from "./DivLogin.vue";
import useLoginForm from "@/use/useLoginForm";
import { useAuthStore } from "@/stores/useAuthStore";
import router from "@/router";
import { computed, onMounted } from "vue";
import Loader from "../Loader.vue";
import { storeToRefs } from "pinia";
import AppErrorMsg from "../AppErrorMsg.vue";
import axios from "axios";
const authStore = useAuthStore();
const { isLoading, getError, isAuth } = storeToRefs(useAuthStore());
const isLoad = computed(() => {
  authStore.isLoading;
});
const {
  email,
  firstname,
  lastname,
  name,
  nickname,
  password,
  region,
  status,
  dt,
  isSubmitting,
} = useLoginForm();
const props = defineProps({
  mode: String,
});
const login = async () => {
  try {
    if (props.mode === "reg") {
      const formstate = {
        email: email.value,
        password: password.value,
        nickName: nickname.value,
        info: {
          name: name.value,
          surname: firstname.value,
          patronymic: lastname.value,
          role: { id: status.value },
          region: region.value,
          birthday: dt.value,
        },
      };
      const response = await authStore.login(
        "http://10.8.0.23:8000/api/auth/register/",
        formstate
      );
      if (response.success) {
        console.log(formstate);
        router.push("/");
      } else {
        console.error("Registration failed", response.error);
      }
    } else {
      const formstate = {
        username: email.value,
        password: password.value,
      };
      console.log("log", formstate);
      const response = await authStore.login(
        "http://10.8.0.23:8000/api/auth/login/",
        formstate
      );
      console.log("log1", response);
      if (isAuth) {
        router.push("/");
      } else {
        console.error("Login failed", response.error);
      }
    }
  } catch (error) {
    console.error("An error occurred:", error);
  }
};
</script>
<style scoped>
.error-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(255, 255, 255, 0.9);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
  backdrop-filter: blur(2px);
}
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1000;
}
button {
  padding: 10px;
  font-size: 16px;
  border: none;
  background-color: var(--fon);
  width: 200px;
  font-weight: 600;
  color: var(--sin);
  border-radius: 6px;
  cursor: pointer;
  margin-top: auto;
  align-self: flex-end;
}
button:hover {
  color: white;
  background-color: var(--sin);
  transition: all 0.5s ease;
}
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

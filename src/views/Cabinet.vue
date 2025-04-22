<template>
  <div>
    <div v-if="loading" class="loader-overlay"><Loader /></div>
    <div class="containerInfo">
      <InfoUser :data="userData" /> <InfoCommandUser />
    </div>
  </div>
</template>
<script setup>
import Loader from "@/components/Loader.vue";
import InfoCommandUser from "@/components/user/infoCommandUser.vue";
import InfoUser from "@/components/user/InfoUserPD.vue";
import getUser from "@/use/useGetUser";
import { onMounted, ref } from "vue";
const token = ref("");
const loading = ref();
const userData = ref();
onMounted(async () => {
  try {
    loading.value = true;
    token.value = localStorage.getItem("jwtToken");
    if (!token.value) {
      throw new Error("Токен не найден");
    }
    userData.value = await getUser(token.value);
  } catch (error) {
    console.error("Ошибка при загрузке пользователя:", error);
  } finally {
    loading.value = false;
  }
});
</script>
<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 1000;
}
.containerInfo {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
</style>

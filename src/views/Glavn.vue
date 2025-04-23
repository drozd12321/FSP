<template>
  {{ act.value }}

  <div>
    glavn
    {{ getMsg.value }}
  </div>
</template>
<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
import { computed, onMounted, ref } from "vue";
const act = ref();
onMounted(() => {
  act.value = JSON.parse(localStorage.getItem("lastMessage"));
  console.log(act.value);
});
</script>
<style scoped></style>

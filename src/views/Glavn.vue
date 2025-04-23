<template></template>

<script setup>
import { ref, onMounted } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
const act = ref(null);

onMounted(() => {
  act.value = JSON.parse(localStorage.getItem("lastMessage"));
});
</script>

<style scoped></style>

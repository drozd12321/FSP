<template>
  {{ act }}
  <AppMsg :act="act" />
  <div>glavn</div>
</template>
<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
import { computed } from "vue";
const { getMsg } = storeToRefs(useAuthStore());
const act = computed(() => {
  return getMsg.value;
});
</script>
<style scoped></style>

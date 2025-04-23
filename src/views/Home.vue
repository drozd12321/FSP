<template>
  {{ act1 }}
  <div><AppMsg v-if="act1?.show" :act="act1" />Home</div>
</template>
<script setup>
import AppMsg from "@/components/message/AppMsg.vue";
import { computed, onMounted, ref } from "vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
const { getMsg } = storeToRefs(useAuthStore());
const act1 = computed(() => {
  return getMsg.value;
});
</script>
<style scoped></style>

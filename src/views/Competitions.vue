<template>
  <!-- <div><CardInfoComp /></div> -->
  <div class="card"><ListCard /></div>
  {{ getError }}
</template>
<script setup>
import AppErrorMsg from "@/components/AppErrorMsg.vue";
import ListCard from "@/components/ListCard.vue";
import { useAuthStore } from "@/stores/useAuthStore";
import { storeToRefs } from "pinia";
const { getError } = storeToRefs(useAuthStore());
</script>
<style scoped>
.card {
  display: flex;
  flex-direction: column;
  margin: auto;
  width: 1500px;
}
</style>

<template>
  <!-- <div><CardInfoComp /></div> -->
  <div class="card"><ListCard /></div>
</template>
<script setup>
import CardInfoComp from "@/components/CardInfoComp.vue";
import ListCard from "@/components/ListCard.vue";
import Loader from "@/components/Loader.vue";
</script>
<style scoped>
.card {
  display: flex;
  flex-direction: column;
  margin: auto;
  width: 1500px;
}
</style>

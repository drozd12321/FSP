<template>
  <div class="region-detail">
    <h2>Информация о регионе: {{ regionName }}</h2>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const route = useRoute();
const regionName = computed(() => route.params.name);
</script>

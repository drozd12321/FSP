<template>
  <component :is="lay">
    <RouterView></RouterView>
  </component>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
const route = useRoute();
const metalay = route.meta.layout;
const lay = computed(() => {
  const layoutName = `${route.meta.layout}Layout`;
  return layoutName;
});
</script>
<style scoped></style>

<template>
  <TheHead />
  <RouterView v-slot="{ Component }">
    <Transition name="fade">
      <component :is="Component" :key="route.fullPath" />
    </Transition>
  </RouterView>
</template>
<script setup>
import TheHead from "@/components/TheHead.vue";
import { useRoute } from "vue-router";
const route = useRoute();
</script>
<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.1s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

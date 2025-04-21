<template>
  <component :is="lay">
    <RouterView></RouterView>
  </component>
</template>
<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";
import MainLayout from "./Layout/MainLayout.vue";
import AuthLayout from "./Layout/AuthLayout.vue";

const route = useRoute();
const lay = computed(() => {
  const layoutName = route.meta.layout;
  if (layoutName === "Main") {
    return MainLayout;
  } else if (layoutName === "Auth") {
    return AuthLayout;
  }
  return null;
});
</script>
<style scoped></style>

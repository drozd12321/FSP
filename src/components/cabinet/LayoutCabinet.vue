<template>
  <div>
    <div class="containerInfo">
      <div class="sidebar">
        <Sidebar />
      </div>
      <div class="info">
        <RouterView> </RouterView>
      </div>
    </div>
  </div>
</template>
<script setup>
import Sidebar from "@/components/cabinet/Sidebar.vue";
</script>
<style scoped>
.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 1000;
}
.containerInfo {
  display: grid;
  grid-template-areas: "sidebar  info info info";
}
.sidebar {
  grid-area: sidebar;
}
.info {
  grid-area: info;
}
</style>

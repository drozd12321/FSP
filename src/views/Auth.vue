<template>
  <div class="wrapper">
    <div class="cont">
      <div class="head">
        <transition name="fade" mode="out-in">
          <TheHeadAuth :key="mode" :mode="mode" @mode="setMode" />
        </transition>
      </div>
      <AppForm :mode="mode" />
    </div>
  </div>
</template>

<script setup>
import AppForm from "@/components/Auth/AppForm.vue";
import TheHeadAuth from "@/components/Auth/TheHeadAuth.vue";
import { ref } from "vue";
const mode = ref("reg");
const setMode = (newMode) => {
  mode.value = newMode;
};
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
  transform: translateY(0);
}

.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e8eb 100%);
}

.cont {
  display: flex;
  flex-direction: column;
  width: 100%;
  max-width: 700px;
  background-color: white;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
}

.head {
  padding: 20px;
  background: white;
  box-shadow: 0 2px 8px rgba(0, 98, 255, 0.1);
}

.name {
  padding: 12px 0;
  text-align: center;
  font-weight: 600;
  color: #333;
  transition: all 0.3s ease;
  border-radius: 8px;
}

.active {
  background: linear-gradient(135deg, #0062ff 0%, #0038a3 100%);
  color: white;
  box-shadow: 0 4px 12px rgba(0, 98, 255, 0.2);
}

.frm {
  padding: 0 20px 20px;
}

.head:hover {
  box-shadow: 0 4px 12px rgba(0, 98, 255, 0.15);
}

.name:hover:not(.active) {
  color: #0062ff;
  transform: translateY(-2px);
}
</style>

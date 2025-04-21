<template>
  <div class="wrapper">
    <div class="cont">
      <div class="head">
        <div
          class="name"
          @click="setMode('reg')"
          :class="{ active: mode === 'reg' }"
        >
          Регистрация
        </div>
        <div
          class="name"
          @click="setMode('log')"
          :class="{ active: mode === 'log' }"
        >
          Вход
        </div>
      </div>
      <AppForm :mode="mode" />
    </div>
  </div>
</template>
<script setup>
import AppForm from "@/components/Auth/AppForm.vue";
import { ref } from "vue";
const mode = ref("reg");
const setMode = (newMode) => {
  mode.value = newMode;
};
</script>
<style scoped>
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}
.cont {
  display: grid;
  justify-content: center;
  align-items: center;
  height: 830px;
  padding: 20px;
  width: 800px;
  background-color: #fff;
  grid-template-areas:
    "head head"
    "frm frm"
    "reg reg";
}
.head {
  grid-area: head;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  padding: 5px;
  cursor: pointer;
  transition: all 0.4s ease;
  gap: 20px;
  padding: 2px;
  border-radius: 6px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}
.name {
  padding: 10px 40px;
  text-align: center;
}
.frm {
  grid-area: frm;
  width: 100%;
  height: 100%;
}
.active {
  border-radius: 6px;
  background-color: var(--red);
  color: white;
}
</style>

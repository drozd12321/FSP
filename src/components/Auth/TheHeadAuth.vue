<template>
  <div class="block">
    <div
      class="name"
      @click="$emit('mode', 'reg')"
      :class="{ active: mode === 'reg' }"
    >
      Регистрация
    </div>
    <div
      class="name"
      @click="$emit('mode', 'log')"
      :class="{ active: mode === 'log' }"
    >
      Вход
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  mode: String,
});
const emit = defineEmits(["mode"]);
</script>
<style scoped>
.block {
  display: grid;
  margin: auto;
  grid-template-columns: repeat(2, 1fr);
  width: 80%;
}
.name {
  padding: 10px 40px;
  text-align: center;
  background-color: var(--sin);
  border-radius: 6px;
  color: white;
}
.active {
  border-radius: 6px;
  background-color: var(--red);
  color: white;
}
</style>

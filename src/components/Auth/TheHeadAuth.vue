<template>
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
</template>
<script setup>
const props = defineProps({
  mode: String,
});
const emit = defineEmits(["mode"]);
</script>
<style scoped>
.name {
  padding: 10px 40px;
  text-align: center;
}
.active {
  border-radius: 6px;
  background-color: var(--red);
  color: white;
}
</style>

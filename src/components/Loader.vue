<template>
  <l-trefoil
    :size="size"
    :stroke="stroke"
    :stroke-length="strokeLength"
    :bg-opacity="bgOpacity"
    :speed="speed"
    :color="color"
  ></l-trefoil>
</template>

<script setup>
import { trefoil } from "ldrs";
trefoil.register();

const props = defineProps({
  size: {
    type: [String, Number],
    default: 40,
    validator: (value) => !isNaN(Number(value)),
  },
  stroke: {
    type: [String, Number],
    default: 4,
    validator: (value) => !isNaN(Number(value)),
  },
  strokeLength: {
    type: [String, Number],
    default: 0.15,
    validator: (value) => !isNaN(Number(value)),
  },
  bgOpacity: {
    type: [String, Number],
    default: 0.1,
    validator: (value) => !isNaN(Number(value)),
  },
  speed: {
    type: [String, Number],
    default: 1.4,
    validator: (value) => !isNaN(Number(value)),
  },
  color: {
    type: String,
    default: "black",
  },
});
</script>

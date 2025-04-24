import { ref } from "vue";

export const hoverRegion = ref(null);
export const tooltip = ref({
  visible: false,
  text: "",
  x: 0,
  y: 0,
});
export function showTooltip(name, event) {
  hoverRegion.value = name;
  tooltip.value.text = name;
  tooltip.value.visible = true;
  updateTooltipPosition(event);
}

export function hideTooltip() {
  hoverRegion.value = null;
  tooltip.value.visible = false;
}
export function updateTooltipPosition(event) {
  tooltip.value.x = event.clientX + 10;
  tooltip.value.y = event.clientY + 10;
}

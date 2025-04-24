<template>
  <div class="map-wrap">
    <svg viewBox="0 0 512.483 350" preserveAspectRatio="xMidYMid meet">
      <g transform="scale(0.5176595959595959) translate(0, 41.55999418517301)">
        <path
          v-for="region in russia"
          :key="region.id"
          :data-tooltip="region.name"
          :d="region.d"
          :stroke-width="region.strokewidth"
          :stroke-linecap="region.strokelinecap"
          :stroke-linejoin="region.strokelinejoin"
          :stroke-opacity="region.strokeopacity"
          :fill="region.fill"
          original="#3175b5"
          :id="region.id"
          class="jvectormap-region"
          @mouseover="showTooltip(region.name, $event)"
          @mouseleave="hideTooltip"
          :class="{
            hovered: activeCity === region.name,
            check: region.isCheck,
          }"
        />
      </g>
    </svg>
    <div
      v-if="tooltip.visible"
      class="tooltip"
      :style="{ top: tooltip.y + 'px', left: tooltip.x + 'px' }"
    >
      {{ tooltip.text }}
    </div>
  </div>
</template>

<script setup>
import { showTooltip, hideTooltip, tooltip } from "@/use/useHover";
import russia from "../../data/russia";
import { useRouter } from "vue-router";

const router = useRouter();
const props = defineProps({
  activeCity: String,
});
</script>

<style scoped>
/* Ваши существующие стили без изменений */
.check {
  fill: #f7f7f7 !important;
  stroke: #fff;
}

.jvectormap-region {
  cursor: pointer;
  transition: all 0.3s ease;
}
.jvectormap-region:hover,
.hovered {
  fill: #bec7cf;
}

.map-wrap svg {
  width: 100%;
  height: 700px;
}
.tooltip {
  position: fixed;
  background-color: rgba(0, 0, 0, 0.75);
  color: white;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  pointer-events: none;
  white-space: nowrap;
  z-index: 1000;
  user-select: none;
}
</style>

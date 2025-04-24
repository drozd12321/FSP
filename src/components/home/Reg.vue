<template>
  <div class="region-main">
    <h2>Выберите регион:</h2>
    <ul>
      <li v-for="region in regions" :key="region.id">
        <RouterLink :to="`/region/${region.slug}`">
          {{ region.name }}
        </RouterLink>
      </li>
    </ul>
  </div>
</template>

<script setup></script>

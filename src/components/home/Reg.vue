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

<script setup>
const regions = [
  { id: 1, name: "Москва", slug: "moscow" },
  { id: 2, name: "Санкт-Петербург", slug: "spb" },
  // ... другие регионы
];
</script>

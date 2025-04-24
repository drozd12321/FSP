<template>
  <AppFilterCompititions :comp="filteredData" @filterChange="handleFilter" />
  <AppMsg v-if="act" :act="act" />
  <div class="container">
    <div v-if="getCreating" class="loader-overlay">
      <AddCommand @close="close" />
    </div>
    <div v-if="dataLoad" class="loader-overlay"><Loader /></div>
    <div class="card" v-for="com in filteredData">
      <ListCard
        :name="com.name"
        :typeComp="com.competition_type_display"
        :typeCommand="com.type_display"
        :status="com.status"
        :dataregStart="com.dates.registration_start"
        :dataregEnd="com.dates.registration_end"
        :dataStart="com.dates.start_date"
        :dataEnd="com.dates.end_date"
        :disciplName="com.discipline_name"
        :id="com.id"
        :key="com.id"
      />
    </div>
  </div>
</template>
<script setup>
import { useCommandStore } from "@/stores/storeCommand";
import { storeToRefs } from "pinia";
import { debounce } from "lodash-es";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import AppFilterCompititions from "@/components/compititions/AppFilterCompititions.vue";
import ListCard from "@/components/compititions/ListCard.vue";
import AddCommand from "@/components/command/AddCommand.vue";
import Loader from "@/components/Loader.vue";

const { getCreating, getMsg } = storeToRefs(useCommandStore());
const comStore = useCommandStore();
const comp = ref();
const dataLoad = ref(false);
const filteredData = ref();

const handleFilter = debounce((filters) => {
  console.log(filters);
  filteredData.value = comp.value.filter((item) => {
    // Фильтрация по поиску
    const searchMatch =
      !filters.search ||
      item.name.toLowerCase().includes(filters.search.toLowerCase());

    // Фильтрация по статусу
    const statusMatch = !filters.status || item.status === filters.status;

    // Фильтрация по формату участия
    const formatMatch = !filters.format || item.type === filters.format;
    // Фильтрация по формату участия
    const oflineMatch =
      !filters.ofline || item.competition_type === filters.ofline;
    // Фильтрация по региону (предполагаем, что поле называется region_id)
    const regionMatch =
      !filters.region ||
      item.permissions.some((perm) => perm == filters.region);
    // Фильтрация по дате (используем dates.start_date)
    const dateMatch = () => {
      if (!filters.start_date && !filters.end_date) return true;

      const itemDate = new Date(item.dates.start_date);
      const start = filters.start_date ? new Date(filters.start_date) : null;
      const end = filters.end_date ? new Date(filters.end_date) : null;

      if (start && itemDate < start) return false;
      if (end && itemDate > end) return false;

      return true;
    };

    return (
      searchMatch &&
      statusMatch &&
      oflineMatch &&
      formatMatch &&
      regionMatch &&
      dateMatch()
    );
  });
}, 300);
const getCompititions = async () => {
  try {
    dataLoad.value = true;
    const response = await axios.get("http://10.8.0.23:8000/competitions/");
    filteredData.value = response.data;
    comp.value = response.data;
    console.log(comp.value);
    dataLoad.value = false;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    dataLoad.value = false;
    throw error;
  }
};
const close = () => {
  comStore.setCreating(false);
};
const act = computed(() => {
  return getMsg.value;
});
const create = computed(() => {
  return getCreating.value;
});
onMounted(() => {
  getCompititions();
});
</script>
<style scoped>
.container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 4rem;
  max-width: 1500px;
  margin: 0 auto;
  padding: 1rem;
}

.card {
  width: 100%;

  transition: all 0.5s ease;
  border-radius: 5px;
}

.loader-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: rgba(255, 255, 255, 0.8);
  z-index: 100;
}
.card:hover {
  transform: translateY(-7px);
  box-shadow: 0 4px 10px black;
}
</style>

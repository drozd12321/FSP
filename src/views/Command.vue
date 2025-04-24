<template>
  <div>
    <div v-if="load" class="loader-overlay"><Loader /></div>
    <div class="flt">
      <FilterCommand @filter="applyFilters" @reset="resetFilters" />
    </div>
    <div v-for="com in filteredComands" :key="com.id">
      <AppCardInfoCommand
        :nameCommand="com.name"
        :nameCompitition="com.competition.name"
        :description="com.description"
        :captain="com.captain.nickName"
        :startData="com.competition.dates.start_date"
        :endData="com.competition.dates.end_date"
        :maxMembers="com.max_members"
        :curentMembers="com.current_members"
        :registrationStart="com.competition.dates.registration_start"
        :id="com.competition.id"
      />
    </div>
  </div>
</template>

<script setup>
import AppCardInfoCommand from "@/components/command/AppCardInfoCommand.vue";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
import Loader from "@/components/Loader.vue";
import FilterCommand from "@/components/command/FilterCommand.vue";

const { getLoading } = storeToRefs(competitionStore());
const comand = ref([]);
const load = ref(false);
const filters = ref({
  searchQuery: "",
  competition: null,
  dateRange: null,
  // добавьте другие поля фильтрации по необходимости
});

const getCommand = async () => {
  try {
    load.value = true;
    const response = await axios.get("http://10.8.0.23:8000/teams/public/");
    comand.value = response.data.teams;
    load.value = false;
    return response.data;
  } catch (error) {
    load.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};

const filteredComands = computed(() => {
  return comand.value.filter((team) => {
    // Фильтрация по поисковому запросу
    if (filters.value.searchQuery) {
      const searchLower = filters.value.searchQuery.toLowerCase();
      if (
        !team.name.toLowerCase().includes(searchLower) &&
        !team.description.toLowerCase().includes(searchLower) &&
        !team.captain.nickName.toLowerCase().includes(searchLower)
      ) {
        return false;
      }
    }

    // Фильтрация по соревнованию
    if (
      filters.value.competition &&
      team.competition.id !== filters.value.competition
    ) {
      return false;
    }

    // Фильтрация по дате
    if (filters.value.dateRange) {
      const startDate = new Date(team.competition.dates.start_date);
      const endDate = new Date(team.competition.dates.end_date);

      if (
        filters.value.dateRange.start &&
        startDate < new Date(filters.value.dateRange.start)
      ) {
        return false;
      }
      if (
        filters.value.dateRange.end &&
        endDate > new Date(filters.value.dateRange.end)
      ) {
        return false;
      }
    }

    return true;
  });
});

const applyFilters = (newFilters) => {
  filters.value = { ...filters.value, ...newFilters };
};

const resetFilters = () => {
  filters.value = {
    searchQuery: "",
    competition: null,
    dateRange: null,
  };
};

onMounted(() => {
  getCommand();
});
</script>

<style scoped>
.loader-overlay {
  display: flex;
  justify-content: center;
  height: 400px;
}
</style>

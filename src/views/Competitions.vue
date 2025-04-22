<template>
  <div class="container">
    <div v-if="dataLoad" class="loader-overlay"><Loader /></div>
    <div class="card" v-for="com in comp">
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
import ListCard from "@/components/ListCard.vue";
import Loader from "@/components/Loader.vue";
import axios from "axios";
import { onMounted, ref } from "vue";
const comp = ref();
const dataLoad = ref(false);
const getCompititions = async () => {
  try {
    dataLoad.value = true;
    const response = await axios.get("http://10.8.0.23:8000/competitions/");
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
  background-color: rgba(255, 255, 255, 0.7);
  z-index: 1000;
}
.card:hover {
  transform: translateY(-7px);
  box-shadow: 0 4px 10px black;
}
</style>

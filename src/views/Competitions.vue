<template>
  <!-- <div><CardInfoComp /></div> -->
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
    />
  </div>
</template>
<script setup>
import AddCompetition from "@/components/AddCompetition.vue";
import AppErrorMsg from "@/components/AppErrorMsg.vue";
import ListCard from "@/components/ListCard.vue";
import { useAuthStore } from "@/stores/useAuthStore";
import axios from "axios";
import { storeToRefs } from "pinia";
import { onMounted, ref } from "vue";
const { getError, getUser } = storeToRefs(useAuthStore());
const comp = ref();
const getCompititions = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/competitions/");
    comp.value = response.data;
    console.log(comp.value);
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getCompititions();
});
</script>
<style scoped>
.card {
  display: flex;
  flex-direction: column;
  margin: 1rem auto;
  width: 1500px;
}
</style>

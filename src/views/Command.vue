<template>
  <div>
    <div v-if="load" class="loader-overlay"><Loader /></div>
    <div v-for="com in comand">
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
      />
    </div>
  </div>
</template>
<script setup>
import AddCommand from "@/components/AddCommand.vue";
import AppCardInfoCommand from "@/components/command/AppCardInfoCommand.vue";
import axios from "axios";
import { computed, onMounted, ref } from "vue";
import { competitionStore } from "@/stores/storeComp";
import { storeToRefs } from "pinia";
import Loader from "@/components/Loader.vue";
const { getLoading } = storeToRefs(competitionStore());
const comand = ref();
const load = ref(false);
const getCommand = async () => {
  try {
    load.value = true;
    const response = await axios.get("http://10.8.0.23:8000/teams/public/");
    comand.value = response.data.teams;
    console.log(comand.value);
    console.log(comand);
    load.value = false;
    return response.data;
  } catch (error) {
    load.value = false;
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getCommand();
});
</script>
<style scoped>
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
</style>

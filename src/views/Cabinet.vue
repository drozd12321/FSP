<template>
  <InfoUser :data="userData" />
</template>
<script setup>
import AddCompetition from "@/components/AddCompetition.vue";
import Sidebar from "@/components/cabinet/Sidebar.vue";
import Loader from "@/components/Loader.vue";
import InfoCommandUser from "@/components/user/infoCommandUser.vue";
import InfoUser from "@/components/user/InfoUserPD.vue";
import getUser from "@/use/useGetUser";
import { onMounted, ref } from "vue";
</script>
<style scoped></style>

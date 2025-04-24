import { computed, ref } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useAuthStore } from "./useAuthStore";

export const useMsgStore = defineStore("msg", () => {
  const msg = ref({
    show: false,
    type: "",
    title: "",
  });

  function setMesg(newVal) {
    msg.value.show = newVal.show;
    msg.value.title = newVal.title;
    msg.value.type = newVal.type;
  }

  const getMsg = computed(() => msg.value);

  return {
    getMsg,
    setMesg,
  };
});

<template>
  <h2>Регистрация</h2>
  <div class="inpdiv">
    <label class="label" for="email">Email</label>
    <input
      type="text"
      id="email"
      :value="emailVal"
      @input="$emit('update:emailVal', $event.target.value)"
    />
  </div>
  <div class="inpdiv">
    <label class="label" for="password">Пароль</label>
    <input
      type="password"
      id="password"
      :value="passwordVal"
      @input="$emit('update:passwordVal', $event.target.value)"
    />
  </div>
  <div class="fio">
    <div class="inpdiv">
      <label class="label" for="name">Имя</label>
      <input
        type="text"
        id="name"
        :value="nameVal"
        @input="$emit('update:nameVal', $event.target.value)"
      />
    </div>
    <div class="inpdiv">
      <label class="label" for="fam">Фамилия</label>
      <input
        type="text"
        id="fam"
        :value="firstnameVal"
        @input="$emit('update:firstnameVal', $event.target.value)"
      />
    </div>
    <div class="inpdiv">
      <label class="label" for="otch">Отчество</label>
      <input
        type="text"
        id="otch"
        :value="lastnameVal"
        @input="$emit('update:lastnameVal', $event.target.value)"
      />
    </div>
  </div>
  <div class="inpdiv">
    <label class="label" for="nickname">NiсkName</label>
    <input
      type="nickname"
      id="nickname"
      :value="nicknameVal"
      @input="$emit('update:nicknameVal', $event.target.value)"
    />
  </div>
  <div class="inpdiv">
    <label class="label" for="status">Статус</label>
    <select
      name="status"
      id="status"
      :value="statusVal"
      @input="$emit('update:statusVal', $event.target.value)"
    >
      <option v-for="rol in roles" :value="rol.id">{{ rol.name }}</option>
    </select>
  </div>
  <div class="inpdiv">
    <label class="label" for="email">Регион</label>
    <select
      name="region"
      id="region"
      :value="regionVal"
      @input="$emit('update:regionVal', $event.target.value)"
    >
      <option v-for="reg in regions" :value="reg.id">{{ reg.name }}</option>
    </select>
  </div>
  <div class="inpdiv">
    <label class="label" for="data"> Дата Рождения</label>
    <input
      type="date"
      id="data"
      :value="dtVal"
      @input="$emit('update:dtVal', $event.target.value)"
    />
  </div>
</template>
<script setup>
import region from "@/data/region";
import axios from "axios";
import { onMounted, ref } from "vue";
const emit = defineEmits([
  "update:emailVal",
  "update:passwordVal",
  "update:dtVal",
  "update:firstnameVal",
  "update:lastnameVal",
  "update:nameVal",
  "update:regionVal",
  "update:statusVal",
  "update:nicknameVal",
  "submit",
]);
const props = defineProps({
  mode: String,
  emailVal: String,
  passwordVal: String,
  dtVal: String,
  firstnameVal: String,
  lastnameVal: String,
  nicknameVal: String,
  nameVal: String,
  regionVal: String,
  statusVal: String,
  isSubmitting: Boolean,
  istomanyAttemots: Boolean,
});
const regions = ref();
const roles = ref();
const getRegion = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/regions/");

    regions.value = response.data;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
const getRoles = async () => {
  try {
    const response = await axios.get("http://10.8.0.23:8000/roles/");

    roles.value = response.data;
    return response.data;
  } catch (error) {
    console.error("Error fetching regions:", error);
    throw error;
  }
};
onMounted(() => {
  getRegion();
  getRoles();
});
</script>
<style scoped>
*,
*::before,
*::after {
  box-sizing: border-box;
}
.fio {
  display: grid;
  grid-template-areas: "name firstname lastname";
  align-items: center;
  gap: 20px;
}
.fio .inpdiv {
  flex: 1;
}
.inpdiv {
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* чтобы поля занимали равную высоту */
  justify-content: center;
}

input {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #aaa;
  border-radius: 4px;
  width: 100%;
  transition: all 0.3s ease;
  outline: none;
}
select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #aaa;
  border-radius: 4px;
  width: 100%;
  background-color: white;
}
input:focus {
  border: 1px solid var(--sin);
}
select:focus {
  border: 1px solid var(--sin);
}
button {
  padding: 10px;
  font-size: 16px;
  border: none;
  background-color: var(--fon);
  width: 200px;
  font-weight: 600;
  color: var(--sin);
  border-radius: 6px;
  cursor: pointer;
  margin-top: auto;
  align-self: flex-end;
}
button:hover {
  color: white;
  background-color: var(--sin);
  transition: all 0.5s ease;
}
button:disabled {
  background-color: #aaa;
}
.reg {
  grid-area: reg;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
}
.reg h3 {
  text-align: center;
}
.one {
  display: flex;
  justify-content: space-around;
}
</style>

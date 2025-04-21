<template>
  <h2>Регистрация</h2>
  <div class="inpdiv">
    <label class="label" for="email">Email</label>
    <input type="email" id="email" />
  </div>
  <div class="inpdiv">
    <label class="label" for="password">Пароль</label>
    <input type="password" id="password" />
  </div>
  <div class="fio">
    <div class="inpdiv">
      <label class="label" for="name">Имя</label>
      <input type="text" id="name" />
    </div>
    <div class="inpdiv">
      <label class="label" for="fam">Фамилия</label>
      <input type="text" id="fam" />
    </div>
    <div class="inpdiv">
      <label class="label" for="otch">Отчество</label>
      <input type="text" id="otch" />
    </div>
  </div>
  <div class="inpdiv">
    <label class="label" for="nickname">NiсkName</label>
    <input type="nickname" id="nickname" />
  </div>
  <div class="inpdiv">
    <label class="label" for="status">Статус</label>
    <select name="status" id="status">
      <option value="fsp">Представитель ФСП</option>
      <option value="fspReg">Региональный представитель ФСП</option>
      <option value="user">Участник</option>
    </select>
  </div>
  <div class="inpdiv">
    <label class="label" for="email">Регион</label>
    <select name="region" id="region"></select>
  </div>
  <div class="inpdiv">
    <label class="label" for="email"> Дата Рождения</label>
    <input />
  </div>
  <button type="submit">Войти</button>
  <div class="reg">
    <h3>Зарегистрироваться через</h3>
    <div class="one">
      <div>
        <span>Госуслуги</span>
      </div>
      <div><span>Google</span></div>
      <div><span>Соц Сети</span></div>
    </div>
  </div>
</template>
<script setup></script>
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

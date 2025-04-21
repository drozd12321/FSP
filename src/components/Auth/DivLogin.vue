<template>
  <h2>Войти в систему</h2>
  <div class="inpdiv">
    <label class="label" for="email">Email:</label>
    <input type="email" id="email" />
  </div>
  <div class="inpdiv">
    <label class="label" for="password">Password:</label>
    <input type="password" id="password" />
  </div>
  <button type="submit">Войти</button>
  <div class="reg">
    <h3>Войти через</h3>
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

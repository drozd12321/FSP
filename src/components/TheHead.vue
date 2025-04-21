<template>
  <div class="head">
    <div class="one">
      <RouterLink to="/competitions">Соревнования</RouterLink>
    </div>
    <div class="two"><RouterLink to="/command">Поиск команд</RouterLink></div>
    <div class="three"><RouterLink to="/rating">Рейтинг</RouterLink></div>
    <div class="fo"><RouterLink to="/admins">Представители</RouterLink></div>
    <div class="five"><RouterLink to="news">Новости</RouterLink></div>
    <div class="c"><RouterLink to="/FAQ">FAQ</RouterLink></div>
  </div>
</template>
<script setup>
import { useAuthStore } from "@/stores/useAuthStore";
const { isAuth } = useAuthStore();
</script>
<style scoped>
a {
  color: white; /* Цвет текста */
  text-decoration: none; /* Убирает подчеркивание */
  list-style: none;
}
header {
  background-color: var(--fon);
  color: white;
  font-size: 22px;
  cursor: pointer;
}
.hd {
  display: grid;
  grid-template-areas: "img img img cab poch";
  align-items: center;
  text-align: center;
}
.img {
  grid-area: img;
  padding: 25px;
}
.cab {
  grid-area: cab;
  padding: 25px;
}
.poch {
  grid-area: poch;
  padding: 25px;
}
.head {
  color: white;
  background-color: var(--red);
  display: grid;
  grid-template-areas: "one two three fo five five six";
  align-items: center;
  text-align: center;
  cursor: pointer;
}
.one {
  grid-area: one;
  padding: 20px;
}
.two {
  grid-area: two;
  padding: 20px;
}
.three {
  grid-area: three;
  padding: 20px;
}
.fo {
  grid-area: fo;
  padding: 20px;
}
.five {
  grid-area: five;
  padding: 20px;
}
.six {
  grid-area: six;
  padding: 20px;
}
</style>

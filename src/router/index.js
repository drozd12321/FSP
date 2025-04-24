import { createRouter, createWebHistory } from "vue-router";
import Home from "@/views/Home.vue";
import Auth from "@/views/Auth.vue";
import { useAuthStore } from "@/stores/useAuthStore";
import Admins from "@/views/Admins.vue";
import Command from "@/views/Command.vue";
import Competitions from "@/views/Competitions.vue";
import FAQ from "@/views/FAQ.vue";
import Rating from "@/views/Rating.vue";
import News from "@/views/News.vue";
import Cabinet from "@/views/Cabinet.vue";
import CompLayuot from "@/views/CompLayuot.vue";
import LayoutCabinet from "@/components/cabinet/LayoutCabinet.vue";
import InfoCommandUser from "@/components/user/infoCommandUser.vue";
import InfoAllCompititions from "@/components/user/infoAllCompititions.vue";
import InfoCardUserAdmin from "@/components/cabinet/InfoCardUserAdmin.vue";
import InfoCardZavkaProved from "@/components/cabinet/InfoCardZavkaProved.vue";
import InfoIZavka from "@/components/cabinet/InfoIZavka.vue";
import MyInfoZavkaCommand from "@/components/cabinet/MyInfoZavkaCommand.vue";
import MessagePoch from "@/components/pocha/MessagePoch.vue";
import Region from "@/components/home/Region.vue";
import InfReg from "@/components/home/InfReg.vue";
import Reg from "@/components/home/Reg.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home,
      meta: {
        layout: "Main",
        auth: false,
      },
    },
    {
      path: "/admins",
      name: "admins",
      component: Admins,
      meta: {
        layout: "Main",
        auth: false,
      },
    },
    {
      path: "/region",
      name: "region",
      component: Region,
      children: [
        {
          path: "",
          name: "region-main",
          component: Reg,
        },
        {
          path: ":name",
          name: "region-detail",
          component: InfReg,
          props: true,
        },
      ],
    },
    {
      path: "/command",
      name: "command",
      component: Command,
      meta: {
        layout: "Main",
        auth: false,
      },
    },
    {
      path: "/competitions",
      name: "competitions",
      component: CompLayuot,
      meta: {
        layout: "Main",
        auth: false,
      },
      children: [
        {
          path: "",
          name: "list",
          component: Competitions,
        },
      ],
    },
    {
      path: "/rating",
      name: "rating",
      component: Rating,
      meta: {
        layout: "Main",
        auth: false,
      },
    },
    {
      path: "/news",
      name: "news",
      component: News,
      meta: {
        layout: "Main",
        auth: false,
      },
    },
    {
      path: "/FAQ",
      name: "FAQ",
      component: FAQ,
      meta: {
        layout: "Main",
        auth: false,
      },
    },

    {
      path: "/cabinet",
      name: "cabinet",
      component: LayoutCabinet,
      meta: {
        layout: "Main",
        auth: false,
      },
      children: [
        { path: "", name: "pd", component: Cabinet },
        { path: "infocomand", name: "infocomand", component: InfoCommandUser },
        {
          path: "infoallcompetitions",
          name: "infoallcompetitions",
          component: InfoAllCompititions,
        },
        {
          path: "InfoCardUserAdmin",
          name: "InfoCardUserAdmin",
          component: InfoCardUserAdmin,
        },
        {
          path: "InfoCardZavkaProved",
          name: "InfoCarInfoCardZavkaProveddUserAdmin",
          component: InfoCardZavkaProved,
        },
        {
          path: "InfoIZavka",
          name: "InfoIZavka",
          component: InfoIZavka,
        },
        {
          path: "myInfoZavkaCommand",
          name: "MyInfoZavkaCommand",
          component: MyInfoZavkaCommand,
        },
        {
          path: "message",
          name: "message",
          component: MessagePoch,
        },
      ],
    },
    {
      path: "/auth",
      name: "auth",
      component: Auth,
      meta: {
        layout: "Auth",
        auth: false,
      },
    },
  ],
  linkActiveClass: "active",
  linkExactActiveClass: "active",
});
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const authRequired = to.meta.auth;
  if (authRequired && authStore.isAuth) {
    next();
  } else if (authRequired && !authStore.isAuth) {
    next("/auth");
  } else {
    next();
  }
});

export default router;

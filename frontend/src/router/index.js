import { createRouter, createWebHistory } from "vue-router";

import LandingView from "@/views/LandingView.vue";
import DashboardView from "@/views/DashboardView.vue";
import ChildrenView from "@/views/ChildrenView.vue"

const routes = [
  {
    path: "/",
    component: LandingView,
  },

  {
    path: "/dashboard",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/children",
    component: ChildrenView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access");

  if (to.meta.requiresAuth && !token) {
    next("/");
  } else {
    next();
  }
});

export default router;
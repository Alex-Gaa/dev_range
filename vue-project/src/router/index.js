import { createRouter, createWebHistory } from "vue-router";

import LoginView from "../views/LoginView.vue";
import RegisterView from "../views/RegisterView.vue";
import DashboardView from "../views/DashboardView.vue";
import LandingView from "../views/LandingView.vue";
const routes = [
  {
    path: "/",
    component: LandingView,
  },
  {
    path: "/",
    redirect: "/dashboard",
  },

  {
    path: "/login",
    component: LoginView,
  },

  {
    path: "/register",
    component: RegisterView,
  },

  {
    path: "/dashboard",
    component: DashboardView,
    meta: { requiresAuth: true },
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// 🔐 GUARD
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
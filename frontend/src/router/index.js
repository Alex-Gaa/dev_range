//C:\Users\Developer\PycharmProjects\devrange\frontend\src\router\index.js
import { createRouter, createWebHistory } from "vue-router";

import LandingView from "@/views/LandingView.vue";
import DashboardView from "@/views/DashboardView.vue";
import ChildrenView from "@/views/ChildrenView.vue"
import LessonsView from "@/views/LessonsView.vue"
import ChildInviteView from "@/views/ChildInviteView.vue"

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
  {
    path: "/children/:id",
    component: () => import("@/views/ChildDetailView.vue"),
    meta: { requiresAuth: true },
  },
  {
    path: "/lessons",
    component: LessonsView,
    meta: { requiresAuth: true },
  },
  {
    path: "/lessons/:id",
    name: "lesson-detail",
    component: () => import("@/views/LessonDetailView.vue"),
  },

  {
    path: "/child-invite/:token",
    name: "child-invite",
    component: ChildInviteView,
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
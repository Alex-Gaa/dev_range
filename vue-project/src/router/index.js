import { createRouter, createWebHistory } from "vue-router";

/* PUBLIC */
import LandingView from "@/views/LandingView.vue";
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";

/* LAYOUT */
import DashboardLayout from "@/layouts/DashboardLayout.vue";

/* DASHBOARD */
import ProfileView from "@/views/dashboard/ProfileView.vue";
import FeedView from "@/views/dashboard/FeedView.vue";
import CreatePostView from "@/views/dashboard/CreatePostView.vue";
import SettingsView from "@/views/dashboard/SettingsView.vue";
import PostDetailView from "@/views/dashboard/PostDetailView.vue";

const routes = [
  {
    path: "/",
    component: LandingView,
  },

  {
    path: "/login",
    component: LoginView,
  },

  {
    path: "/register",
    component: RegisterView,
  },

  /* =========================
     DASHBOARD
  ========================= */
  {
    path: "/dashboard",
    component: DashboardLayout,
    meta: { requiresAuth: true },

    children: [
      {
        path: "",
        redirect: "/dashboard/feed",
      },

      {
        path: "profile",
        component: ProfileView,
      },

      {
        path: "feed",
        component: FeedView,
      },

      {
        path: "posts/create",
        component: CreatePostView,
      },

      /* 👇 ВАЖНО: пост теперь внутри dashboard */
      {
        path: "posts/:slug",
        component: PostDetailView,
      },

      {
        path: "settings",
        component: SettingsView,
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem("access");

  if (to.meta.requiresAuth && !token) {
    next("/login");
  } else {
    next();
  }
});

export default router;
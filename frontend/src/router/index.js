// C:\Users\Developer\PycharmProjects\devrange\frontend\src\router\index.js

import {
  createRouter,
  createWebHistory,
} from "vue-router"

import LandingView from "@/views/LandingView.vue"
import DashboardView from "@/views/DashboardView.vue"

import ChildrenView from "@/views/ChildrenView.vue"

import LessonsView from "@/views/LessonsView.vue"

import ChildInviteView from "@/views/ChildInviteView.vue"

import ChildProgressView from "@/views/ChildProgressView.vue"

import ChildAchievementsView from "@/views/ChildAchievementsView.vue"

import ChildGoalsView from "@/views/ChildGoalsView.vue"
//import SubjectsView from "@/views/SubjectsView.vue"
import BillingView from "@/views/BillingView.vue"
const routes = [
  {
    path: "/",
    component: LandingView,
  },

  /* DASHBOARD */

  {
    path: "/dashboard",
    component: DashboardView,
    meta: {
      requiresAuth: true,
    },
  },

  /* CHILDREN */

  {
    path: "/children",
    component: ChildrenView,
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/children/:id",
    component: () =>
      import("@/views/ChildDetailView.vue"),

    meta: {
      requiresAuth: true,
    },
  },

//  {
//    path: "/subjects",
//    name: "subjects",
//    component: () => import("@/views/SubjectsView.vue"),
//  },

  /* LESSONS */

  {
    path: "/lessons",
    component: LessonsView,
    meta: {
      requiresAuth: true,
    },
  },
  {
    path: "/lessons/create",
    name: "lesson-create",
    component: () => import("@/views/LessonCreateView.vue"),
    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/lessons/:id",
    name: "lesson-detail",

    component: () =>
      import("@/views/LessonDetailView.vue"),

    meta: {
      requiresAuth: true,
    },
  },

  /* CHILD INVITE */

  {
    path: "/child-invite/:token",
    name: "child-invite",
    component: ChildInviteView,
  },

  /* CHILD PROGRESS */

  {
    path: "/progress",
    component: ChildProgressView,

    meta: {
      requiresAuth: true,
    },
  },

  /* ACHIEVEMENTS */

  {
    path: "/achievements",
    component: ChildAchievementsView,

    meta: {
      requiresAuth: true,
    },
  },

  /* DAILY GOALS */

  {
    path: "/goals",
    component: ChildGoalsView,

    meta: {
      requiresAuth: true,
    },
  },

  {
    path: "/billing",
    component: BillingView,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/* AUTH GUARD */

router.beforeEach((to, from, next) => {

  const token = localStorage.getItem("access")

  if (to.meta.requiresAuth && !token) {

    next("/")

  } else {

    next()
  }
})

export default router
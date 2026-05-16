<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\layouts\AppLayout.vue -->

<template>
  <div class="min-h-screen bg-slate-100 flex">

    <!-- SIDEBAR -->
    <aside
      class="
        w-72
        h-screen
        sticky
        top-0
        bg-white
        border-r
        flex
        flex-col
      "
    >

      <!-- LOGO -->
      <div class="p-6 border-b">

        <h1 class="text-2xl font-bold text-blue-600">
          AI Learning
        </h1>

      </div>

      <!-- NAVIGATION -->
      <nav
        class="
            flex-1
            p-4
            space-y-2
            overflow-y-auto
        "
      >

        <router-link
          v-for="item in menuItems"
          :key="item.path"
          :to="item.path"
          class="
            flex
            items-center
            gap-3
            px-4
            py-3
            rounded-xl
            transition-all
            font-medium
          "
          :class="
            isActive(item.path)
              ? 'bg-blue-600 text-white shadow-md'
              : 'hover:bg-slate-100 text-slate-700'
          "
        >

          <span class="text-lg">
            {{ item.icon }}
          </span>

          <span>
            {{ item.label }}
          </span>

        </router-link>

      </nav>

      <!-- USER -->
      <div class="p-4 border-t">

        <div class="flex items-center gap-3 mb-5">

          <!-- AVATAR -->
          <div
            class="
              w-12
              h-12
              rounded-full
              bg-blue-600
              text-white
              flex
              items-center
              justify-center
              font-bold
              text-lg
              shrink-0
            "
          >

            {{ authStore.user?.first_name?.charAt(0) || "U" }}

          </div>

          <!-- USER INFO -->
          <div class="min-w-0">

            <p class="font-semibold truncate">
              {{ userName }}
            </p>

            <p class="text-sm text-slate-500 capitalize">
              {{ userRole }} account
            </p>

          </div>

        </div>

        <!-- LOGOUT -->
        <button
          @click="logout"
          class="
            w-full
            bg-red-500
            hover:bg-red-600
            text-white
            py-3
            rounded-xl
            transition
          "
        >
          Logout
        </button>

      </div>

    </aside>

    <!-- MAIN -->
    <div class="flex-1 flex flex-col">

      <!-- TOPBAR -->
      <header
        class="
          h-20
          bg-white
          border-b
          flex
          items-center
          px-8
        "
      >

        <div>

          <h2 class="text-2xl font-semibold capitalize">
            {{ userRole }} dashboard
          </h2>

          <p class="text-sm text-slate-500 mt-1">
            Welcome back to AI Learning
          </p>

        </div>

      </header>

      <!-- PAGE CONTENT -->
      <main class="flex-1 p-8">

        <slot />

      </main>

    </div>

  </div>
</template>

<script setup>
import {
  computed,
  onMounted,
} from "vue"

import {
  useRouter,
  useRoute,
} from "vue-router"

import { useAuthStore } from "@/stores/auth"

import { sidebarConfig } from "@/config/sidebar"

const router = useRouter()

const route = useRoute()

const authStore = useAuthStore()

/* LOAD USER */
onMounted(async () => {

  if (!authStore.user) {

    await authStore.fetchMe()
  }
})

/* USER DATA */

const userName = computed(() => {

  if (!authStore.user) {
    return "Guest"
  }

  return `
    ${authStore.user.first_name || ""}
    ${authStore.user.last_name || ""}
  `.trim()
})

const userRole = computed(() => {
  return authStore.user?.role || "parent"
})

/* SIDEBAR ITEMS */

const menuItems = computed(() => {
  return sidebarConfig[userRole.value] || []
})

/* ACTIVE LINK */

const isActive = (path) => {

  if (path === "/dashboard") {

    return route.path === "/dashboard"
  }

  return route.path.startsWith(path)
}

/* LOGOUT */

const logout = () => {

  authStore.logout()

  router.push("/")
}
</script>
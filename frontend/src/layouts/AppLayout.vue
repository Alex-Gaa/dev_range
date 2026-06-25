<!-- src/layouts/AppLayout.vue -->

<template>
  <div class="min-h-screen bg-slate-100 flex">

    <!-- MOBILE OVERLAY -->
    <div
      v-if="sidebarOpen"
      @click="sidebarOpen = false"
      class="fixed inset-0 bg-black/40 z-40 lg:hidden"
    />

    <!-- SIDEBAR -->
    <aside
      :class="[
        sidebarOpen
          ? 'translate-x-0'
          : '-translate-x-full',
        'fixed lg:sticky top-0 left-0 z-50 lg:z-auto h-screen w-72 bg-white border-r flex flex-col transition-transform duration-300 lg:translate-x-0'
      ]"
    >

      <!-- LOGO -->
      <div class="p-6 border-b">

        <router-link
          to="/dashboard"
          @click="sidebarOpen = false"
          class="
            text-2xl
            font-bold
            text-blue-600
            hover:text-blue-700
            transition
            inline-block
          "
        >
          Отличник
        </router-link>

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
          @click="sidebarOpen = false"
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

          <div class="min-w-0">

            <p class="font-semibold truncate">
              {{ userName }}
            </p>

            <p class="text-sm text-slate-500">
              {{ userRoleLabel }}
            </p>

          </div>

        </div>

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
          Выйти
        </button>

      </div>

    </aside>

    <!-- MAIN -->
    <div class="flex-1 flex flex-col min-w-0">

      <!-- TOPBAR -->
      <header
        class="
          h-20
          bg-white
          border-b
          flex
          items-center
          px-4
          md:px-6
          lg:px-8
        "
      >

        <!-- MOBILE MENU BUTTON -->
        <button
          @click="sidebarOpen = true"
          class="
            lg:hidden
            mr-4
            text-2xl
            text-slate-700
          "
        >
          ☰
        </button>

        <div>

          <h2
            class="
              text-xl
              md:text-2xl
              font-semibold

            "
          >
            {{ dashboardTitle }}
          </h2>

          <p class="text-sm text-slate-500 mt-1">
            Добро пожаловать в систему обучения «Отличник»
          </p>

        </div>

      </header>

      <!-- PAGE CONTENT -->
      <main
        class="
          flex-1
          p-4
          md:p-6
          lg:p-8
        "
      >

        <slot />

      </main>

    </div>

  </div>
</template>

<script setup>
import {
  computed,
  onMounted,
  ref,
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

const sidebarOpen = ref(false)

/* LOAD USER */
onMounted(async () => {

  if (!authStore.user) {
    await authStore.fetchMe()
  }
})

/* USER DATA */

const userName = computed(() => {

  if (!authStore.user) {
    return "Гость"
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

const userRoleLabel = computed(() => {

  switch (userRole.value) {

    case "parent":
      return "Родитель"

    case "child":
      return "Ребёнок"

    case "admin":
      return "Администратор"

    default:
      return "Пользователь"
  }
})

const dashboardTitle = computed(() => {

  switch (userRole.value) {

    case "parent":
      return "Панель управления родителя"

    case "child":
      return "Панель управления ученика"

    case "admin":
      return "Панель администратора"

    default:
      return "Панель управления"
  }
})

</script>
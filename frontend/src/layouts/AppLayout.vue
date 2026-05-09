<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\layouts\AppLayout.vue -->>
<template>
  <div class="min-h-screen bg-slate-100 flex">

    <!-- SIDEBAR -->
    <aside class="w-72 bg-white border-r flex flex-col">

      <!-- LOGO -->
      <div class="p-6 border-b">

        <h1 class="text-2xl font-bold text-blue-600">
          AI Learning
        </h1>

      </div>

      <!-- NAVIGATION -->
      <nav class="flex-1 p-4 space-y-2">

      <router-link
        v-for="item in menuItems"
        :key="item.path"
        :to="item.path"
        class="
          block
          px-4
          py-3
          rounded-xl
          hover:bg-slate-100
          transition
        "
      >

        {{ item.label }}

      </router-link>

    </nav>

      <!-- USER -->
      <div class="p-4 border-t">

        <button
          @click="logout"
          class="w-full bg-red-500 hover:bg-red-600 text-white py-3 rounded-xl"
        >
          Logout
        </button>

      </div>

    </aside>

    <!-- MAIN -->
    <div class="flex-1 flex flex-col">

      <!-- TOPBAR -->
      <header class="h-20 bg-white border-b flex items-center justify-between px-8">

        <div>
          <h2 class="text-2xl font-semibold">
            {{ userRole }} dashboard
          </h2>
        </div>

        <div class="flex items-center gap-4">

          <div class="text-right">
            <p class="font-medium">
              {{ userName }}
            </p>

            <p class="text-sm text-slate-500 capitalize">
              {{ userRole }} account
            </p>
          </div>

          <div class="w-12 h-12 rounded-full bg-blue-600 flex items-center justify-center text-white font-bold">

            {{ authStore.user?.first_name?.charAt(0) || "U" }}

          </div>

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
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import { useAuthStore } from "@/stores/auth"
import { sidebarConfig } from "@/config/sidebar"

const router = useRouter()
const authStore = useAuthStore()

// загрузка пользователя при входе в layout
onMounted(() => {
  authStore.fetchMe()
})

/**
 * USER DATA
 */

const userName = computed(() => {
  if (!authStore.user) return "Guest"
  return `${authStore.user.first_name} ${authStore.user.last_name}`
})

const userRole = computed(() => {
  return authStore.user?.role || "parent"
})

/**
 * SIDEBAR MENU (role-based)
 */

const menuItems = computed(() => {
  return sidebarConfig[userRole.value] || []
})

/**
 * LOGOUT
 */

const logout = () => {
  authStore.logout()
  router.push("/")
}
</script>
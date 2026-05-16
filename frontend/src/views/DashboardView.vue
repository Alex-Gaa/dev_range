<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\DashboardView.vue -->
<template>

  <AppLayout>

    <ParentDashboard
      v-if="authStore.user?.role === 'parent'"
    />

    <ChildDashboard
      v-else-if="authStore.user?.role === 'child'"
    />

  </AppLayout>

</template>

<script setup>
import AppLayout from "@/layouts/AppLayout.vue"

import ParentDashboard from "@/views/ParentDashboard.vue"
import ChildDashboard from "@/views/ChildDashboard.vue"

import { useAuthStore } from "@/stores/auth"

const authStore = useAuthStore()
</script>
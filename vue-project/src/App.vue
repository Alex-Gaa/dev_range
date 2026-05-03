<!-- C:\Users\Developer\PycharmProjects\devrange\vue-project\src\App.vue -->
<script setup>
import { useRouter } from "vue-router";
import { useAuthStore } from "./stores/auth";
import { computed, onMounted } from "vue";

const router = useRouter();
const auth = useAuthStore();

// 👉 реактивные данные из Pinia
const isAuth = computed(() => auth.isAuth);
const username = computed(() => auth.fullName);

// 👉 загружаем пользователя при старте
onMounted(async () => {
  if (auth.access) {
    await auth.fetchUser();
  }
});

const logout = () => {
  auth.logout();
  router.push("/login");
};
</script>

<template>
  <div class="layout">
    <!-- HEADER -->
    <header class="header">
      <div class="logo">DEV RANGE</div>

      <nav v-if="!isAuth" class="nav">
        <router-link to="/login">Login</router-link>
        <router-link to="/register">Register</router-link>
      </nav>

      <div v-else class="user">
        <!-- <span>👤 {{ username }}</span> -->
        <button @click="logout">Logout</button>
      </div>
    </header>

    <!-- CONTENT -->
    <main class="content-wrapper">
      <router-view />
    </main>
  </div>
</template>
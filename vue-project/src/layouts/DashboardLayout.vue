<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const goProfile = () => router.push("/dashboard/profile");
const goFeed = () => router.push("/dashboard/feed");
const goCreatePost = () => router.push("/dashboard/posts/create");
const goSettings = () => router.push("/dashboard/settings");
</script>

<template>
  <div class="layout dashboard-layout">
    <!-- SIDEBAR -->
    <aside class="sidebar">
      <h3>DEV RANGE</h3>

      <button @click="goProfile">
        👤 Профиль
      </button>

      <button @click="goFeed">
        📰 Feed
      </button>

      <button @click="goCreatePost">
        ✍️ Create Post
      </button>

      <button @click="goSettings">
        ⚙️ Настройки
      </button>
    </aside>

    <!-- CONTENT -->
    <main class="dashboard-content">
      <router-view />
    </main>
  </div>
</template>
<!-- src/views/dashboard/FeedView.vue -->
<script setup>
import { ref, onMounted } from "vue";
import api from "@/api/axios";

const posts = ref([]);
const loading = ref(false);
const error = ref("");

const fetchPosts = async () => {
  try {
    loading.value = true;

    const res = await api.get("api/posts/");
    posts.value = res.data;
  } catch (err) {
    console.error(err);
    error.value = "Ошибка загрузки постов";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPosts();
});
</script>

<template>
  <div class="feed-page">
    <h1 class="feed-title">Feed</h1>

    <div v-if="loading" class="card">
      <p>Загрузка постов...</p>
    </div>

    <div v-else-if="error" class="error">
      {{ error }}
    </div>

    <div v-else class="feed">
      <div
        v-for="post in posts"
        :key="post.id"
        class="card post-card"
      >
        <!-- ✅ ВАЖНО: теперь dashboard route -->
        <router-link
          :to="`/dashboard/posts/${post.slug}`"
          class="post-link"
        >
          <h2>{{ post.title }}</h2>
        </router-link>

        <p class="excerpt">{{ post.excerpt }}</p>

        <small class="author">
          👤 {{ post.author_name }}
        </small>
      </div>
    </div>
  </div>
</template>
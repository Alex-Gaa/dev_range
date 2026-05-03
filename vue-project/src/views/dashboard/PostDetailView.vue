<script setup>
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/api/axios";
import MarkdownRenderer from "@/views/posts/MarkdownRenderer.vue";

const route = useRoute();
const router = useRouter();

const post = ref(null);
const loading = ref(false);

/* FETCH POST */
const fetchPost = async () => {
  try {
    loading.value = true;

    const res = await api.get(
      `api/posts/${route.params.slug}/`
    );

    post.value = res.data;
  } catch (err) {
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchPost();
});
</script>

<template>
  <div class="post-detail-page">



    <!-- LOADING -->
    <div v-if="loading" class="card">
      <p>Загрузка поста...</p>
    </div>

    <!-- CONTENT -->
    <div v-else-if="post" class="post-detail-card">

      <img
        v-if="post.cover"
        :src="post.cover"
        class="post-cover"
      />

      <div class="post-header">
        <h1>{{ post.title }}</h1>

        <div class="post-detail-meta">
          <span>👤 {{ post.author_name }}</span>
          <span>🛠 {{ post.tech_stack }}</span>
          <span>👁 {{ post.views }}</span>
        </div>
      </div>

      <div v-if="post.excerpt" class="post-excerpt-box">
        {{ post.excerpt }}
      </div>

      <a
        v-if="post.github_url"
        :href="post.github_url"
        target="_blank"
        class="post-github"
      >
        🔗 GitHub
      </a>

      <MarkdownRenderer :content="post.content" />
    </div>

  </div>
</template>
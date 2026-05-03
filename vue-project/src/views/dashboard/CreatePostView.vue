<script setup>
import { reactive, ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/api/axios";
import { useAuthStore } from "@/stores/auth";

const router = useRouter();
const auth = useAuthStore();

const loading = ref(false);
const error = ref("");

/* =========================
   FORM STATE
========================= */
const form = reactive({
  title: "",
  excerpt: "",
  content: "",
  github_url: "",
  tech_stack: "",
});

/* =========================
   CREATE POST
========================= */
const createPost = async () => {
  error.value = "";

  // basic validation
  if (!form.title || !form.content) {
    error.value = "Title и Content обязательны";
    return;
  }

  try {
    loading.value = true;

    const res = await api.post(
      "api/posts/",
      {
        title: form.title,
        excerpt: form.excerpt,
        content: form.content,
        github_url: form.github_url,
        tech_stack: form.tech_stack,
      },
      {
        headers: {
          Authorization: `Bearer ${auth.access}`,
        },
      }
    );

    router.push(`/posts/${res.data.slug}`);
  } catch (err) {
    console.error(err.response?.data);

    error.value = "Ошибка при создании поста";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="create-post-page">
    <div class="card create-post-card">
      <h1>Create Post</h1>

      <!-- ERROR -->
      <div v-if="error" class="error">
        {{ error }}
      </div>

      <!-- INPUTS -->
      <input v-model="form.title" placeholder="Название поста" />

      <input v-model="form.excerpt" placeholder="Краткое описание" />

      <input v-model="form.github_url" placeholder="GitHub URL" />

      <input
        v-model="form.tech_stack"
        placeholder="React, Django, Vue..."
      />

      <!-- MARKDOWN HINT -->
      <div class="editor-hint">
        <h3>Markdown Editor</h3>

        <p>Поддерживается:</p>

        <ul>
          <li>Заголовки (# ## ###)</li>
          <li>Жирный / курсив</li>
          <li>Ссылки</li>
          <li>Изображения</li>
        </ul>

        <p>Код:</p>

        <pre><code>```js
const hello = "world";
```</code></pre>
      </div>

      <!-- CONTENT -->
      <textarea
        v-model="form.content"
        class="post-editor"
        placeholder="Напиши свою историю разработки..."
      ></textarea>

      <!-- SUBMIT -->
      <button
        @click="createPost"
        :disabled="loading"
      >
        {{ loading ? "Публикация..." : "Опубликовать" }}
      </button>
    </div>
  </div>
</template>
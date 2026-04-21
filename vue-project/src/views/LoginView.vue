<!-- C:\Users\Developer\PycharmProjects\devrange\vue-project\src\views\LoginView.vue -->
<!-- LoginView.vue -->
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const username = ref("");
const password = ref("");

const auth = useAuthStore();
const router = useRouter();

const showPassword = ref(false);
const loading = ref(false);

const errorModal = ref(false);
const errorText = ref("");
const error = ref("");

const submit = async () => {
  error.value = "";
  loading.value = true;

  try {
    await auth.login(username.value, password.value);
    router.push("/dashboard");

  } catch (err) {
    console.error(err);

    errorText.value =
      err.response?.data?.detail ||
      "Неверный логин или пароль";

    errorModal.value = true;

  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="content">
    <div class="card">
      <h2>Логин</h2>

      <input v-model="username" placeholder="Email" />

      <div class="password-field">
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Пароль"
        />
        <span class="toggle" @click="showPassword = !showPassword">
          {{ showPassword ? "🙈" : "👁" }}
        </span>
      </div>

      <button @click="submit" :disabled="loading">
        {{ loading ? "Загрузка..." : "Login" }}
      </button>
    </div>

    <!-- MODAL -->
    <div v-if="errorModal" class="modal-overlay">
      <div class="modal">
        <h3>Ошибка</h3>
        <p>{{ errorText }}</p>
        <button @click="errorModal = false">Закрыть</button>
      </div>
    </div>
  </div>
</template>
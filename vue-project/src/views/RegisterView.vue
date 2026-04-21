<!-- C:\Users\Developer\PycharmProjects\devrange\vue-project\src\views\RegisterView.vue -->
<!-- RegisterView.vue -->
<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const first_name = ref("");
const last_name = ref("");
const email = ref("");
const password = ref("");
const password2 = ref("");
const role = ref("developer");

const showPassword = ref(false);
const loading = ref(false);

const errorModal = ref(false);
const errorText = ref("");

const router = useRouter();
const auth = useAuthStore();

const submit = async () => {
  errorText.value = "";

  if (password.value !== password2.value) {
    errorText.value = "Пароли не совпадают";
    errorModal.value = true;
    return;
  }

  loading.value = true;

  try {
    await auth.register({
      first_name: first_name.value,
      last_name: last_name.value,
      email: email.value,
      password: password.value,
      password2: password2.value,
      role: role.value,
    });

    router.push("/dashboard");

  } catch (err) {
    console.error(err);

    errorText.value =
      err.response?.data?.email?.[0] ||
      err.response?.data?.password?.[0] ||
      err.response?.data?.detail ||
      "Ошибка регистрации";

    errorModal.value = true;

  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="content">
    <div class="card">
      <h2>Регистрация</h2>

      <input v-model="first_name" placeholder="Имя" />
      <input v-model="last_name" placeholder="Фамилия" />
      <input v-model="email" placeholder="Email" />

      <div class="password-field">
        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Пароль"
        />
      </div>

      <div class="password-field">
        <input
          v-model="password2"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Повтор пароля"
        />
        <span class="toggle" @click="showPassword = !showPassword">
          {{ showPassword ? "🙈" : "👁" }}
        </span>
      </div>

      <select v-model="role">
        <option value="developer">Developer</option>
        <option value="manager">Manager</option>
      </select>

      <button @click="submit" :disabled="loading">
        {{ loading ? "Создаём..." : "Register" }}
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
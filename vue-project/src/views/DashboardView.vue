<!-- src/views/DashboardView.vue -->
<script setup>
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted, ref, reactive, watch } from "vue";
import api from "@/api/axios";

const auth = useAuthStore();

const user = computed(() => auth.user);
const profile = computed(() => auth.user?.profile);

// sidebar state
const activeTab = ref("profile");

// edit modes
const isEditUser = ref(false);
const isEditProfile = ref(false);

// forms
const userForm = reactive({
  first_name: "",
  last_name: "",
});

const profileForm = reactive({
  bio: "",
  location: "",
  github_url: "",
  linkedin_url: "",
  telegram_url: "",
  portfolio_url: "",
});

// sync user → form
watch(
  user,
  (val) => {
    if (val) {
      userForm.first_name = val.first_name;
      userForm.last_name = val.last_name;
    }
  },
  { immediate: true }
);

// sync profile → form
watch(
  profile,
  (val) => {
    if (val) {
      Object.assign(profileForm, val);
    }
  },
  { immediate: true }
);

onMounted(async () => {
  if (auth.access && !auth.user) {
    await auth.fetchUser();
  }
});

/* =========================
   SAVE USER
========================= */
const saveUser = async () => {
  const res = await api.patch(
    "api/auth/me/",
    {
      first_name: userForm.first_name,
      last_name: userForm.last_name,
    },
    { headers: { Authorization: `Bearer ${auth.access}` } }
  );

  auth.user = res.data;
  isEditUser.value = false;
};

/* =========================
   SAVE PROFILE
========================= */
const saveProfile = async () => {
  const res = await api.patch(
    "api/auth/profile/",
    profileForm,
    { headers: { Authorization: `Bearer ${auth.access}` } }
  );

  auth.user.profile = res.data;
  isEditProfile.value = false;
};
</script>

<template>
  <div class="layout dashboard-layout">
    <!-- ================= SIDEBAR ================= -->
    <aside class="sidebar">
      <h3>DEV RANGE</h3>

      <button
        :class="{ active: activeTab === 'profile' }"
        @click="activeTab = 'profile'"
      >
        👤 Личные данные
      </button>

      <button
        :class="{ active: activeTab === 'settings' }"
        @click="activeTab = 'settings'"
      >
        ⚙️ Настройки
      </button>
    </aside>

    <!-- ================= CONTENT ================= -->
    <main class="dashboard-content">
      <h1>Dashboard</h1>

      <!-- PROFILE TAB -->
      <div v-if="activeTab === 'profile'">
        <div v-if="user" class="card">
          <h2>Профиль пользователя</h2>

          <!-- USER -->
          <div v-if="!isEditUser">
            <p>
              <strong>Имя:</strong>
              {{ user.first_name }} {{ user.last_name }}
            </p>

            <button @click="isEditUser = true">Редактировать</button>
          </div>

          <div v-else>
            <input v-model="userForm.first_name" placeholder="Имя" />
            <input v-model="userForm.last_name" placeholder="Фамилия" />

            <button @click="saveUser">Сохранить</button>
          </div>
        </div>

        <!-- PROFILE -->
        <div v-if="profile" class="card">
          <h2>Доп. информация</h2>

          <div v-if="!isEditProfile">
            <p><strong>Bio:</strong> {{ profile.bio }}</p>
            <p><strong>Location:</strong> {{ profile.location }}</p>

            <button @click="isEditProfile = true">
              Редактировать профиль
            </button>
          </div>

          <div v-else>
            <input v-model="profileForm.bio" placeholder="Bio" />
            <input v-model="profileForm.location" placeholder="Location" />
            <input v-model="profileForm.github_url" placeholder="GitHub" />
            <input v-model="profileForm.linkedin_url" placeholder="LinkedIn" />

            <button @click="saveProfile">Сохранить</button>
          </div>
        </div>
      </div>

      <!-- SETTINGS TAB -->
      <div v-if="activeTab === 'settings'" class="card">
        <h2>Настройки</h2>
        <p>Тут будет позже (смена пароля, удаление аккаунта и т.д.)</p>
      </div>
    </main>
  </div>
</template>
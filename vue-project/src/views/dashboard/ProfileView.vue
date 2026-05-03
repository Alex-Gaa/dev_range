<script setup>
import { useAuthStore } from "@/stores/auth";
import { computed, onMounted, reactive, ref, watch } from "vue";
import api from "@/api/axios";

const auth = useAuthStore();

const user = computed(() => auth.user);
const profile = computed(() => auth.user?.profile);

// edit states
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

// sync user -> form
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

// sync profile -> form
watch(
  profile,
  (val) => {
    if (val) {
      Object.assign(profileForm, val);
    }
  },
  { immediate: true }
);

// fetch user
onMounted(async () => {
  if (auth.access && !auth.user) {
    await auth.fetchUser();
  }
});

/* =========================
   SAVE USER
========================= */
const saveUser = async () => {
  try {
    const res = await api.patch(
      "api/auth/me/",
      {
        first_name: userForm.first_name,
        last_name: userForm.last_name,
      },
      {
        headers: {
          Authorization: `Bearer ${auth.access}`,
        },
      }
    );

    auth.user = {
      ...auth.user,
      ...res.data,
    };

    isEditUser.value = false;
  } catch (err) {
    console.error(err);
  }
};

/* =========================
   SAVE PROFILE
========================= */
const saveProfile = async () => {
  try {
    const res = await api.patch(
      "api/auth/profile/",
      profileForm,
      {
        headers: {
          Authorization: `Bearer ${auth.access}`,
        },
      }
    );

    auth.user.profile = res.data;

    isEditProfile.value = false;
  } catch (err) {
    console.error(err);
  }
};
</script>

<template>
  <div class="profile-page">
    <!-- USER CARD -->
    <div v-if="user" class="card">
      <h2>Профиль пользователя</h2>

      <div v-if="!isEditUser">
        <p>
          <strong>Имя:</strong>
          {{ user.first_name }} {{ user.last_name }}
        </p>

        <p>
          <strong>Email:</strong>
          {{ user.email }}
        </p>

        <p>
          <strong>Роль:</strong>
          {{ user.role }}
        </p>

        <button @click="isEditUser = true">
          Редактировать
        </button>
      </div>

      <div v-else>
        <input
          v-model="userForm.first_name"
          placeholder="Имя"
        />

        <input
          v-model="userForm.last_name"
          placeholder="Фамилия"
        />

        <button @click="saveUser">
          Сохранить
        </button>
      </div>
    </div>

    <!-- PROFILE CARD -->
    <div v-if="profile" class="card">
      <h2>Дополнительная информация</h2>

      <div v-if="!isEditProfile">
        <p>
          <strong>Bio:</strong>
          {{ profile.bio || "—" }}
        </p>

        <p>
          <strong>Location:</strong>
          {{ profile.location || "—" }}
        </p>

        <p>
          <strong>GitHub:</strong>
          {{ profile.github_url || "—" }}
        </p>

        <p>
          <strong>LinkedIn:</strong>
          {{ profile.linkedin_url || "—" }}
        </p>

        <button @click="isEditProfile = true">
          Редактировать профиль
        </button>
      </div>

      <div v-else>
        <input
          v-model="profileForm.bio"
          placeholder="Bio"
        />

        <input
          v-model="profileForm.location"
          placeholder="Location"
        />

        <input
          v-model="profileForm.github_url"
          placeholder="GitHub URL"
        />

        <input
          v-model="profileForm.linkedin_url"
          placeholder="LinkedIn URL"
        />

        <input
          v-model="profileForm.telegram_url"
          placeholder="Telegram URL"
        />

        <input
          v-model="profileForm.portfolio_url"
          placeholder="Portfolio URL"
        />

        <button @click="saveProfile">
          Сохранить профиль
        </button>
      </div>
    </div>
  </div>
</template>
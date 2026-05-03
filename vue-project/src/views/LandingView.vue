<!-- C:\Users\Developer\PycharmProjects\devrange\vue-project\src\views\LandingView.vue -->
<script setup>
import { useRouter } from "vue-router";

const router = useRouter();

const goLogin = () => router.push("/login");
const goRegister = () => router.push("/register");
</script>

<template>
  <div class="landing">

    <!-- HERO -->
    <section class="hero">
      <h1>DEV RANGE</h1>
      <p>Платформа для управления разработкой, командами и проектами</p>

      <div class="hero-actions">
        <button @click="goRegister">Get Started</button>
        <button class="secondary" @click="goLogin">Login</button>
      </div>
    </section>

    <!-- FEATURES -->
    <section class="features">
      <div class="feature">
        <h3>⚡ Fast Workflow</h3>
        <p>Управляй задачами и проектами без хаоса</p>
      </div>

      <div class="feature">
        <h3>👥 Teams</h3>
        <p>Роли: Developer / Manager / Admin</p>
      </div>

      <div class="feature">
        <h3>🔐 Secure Auth</h3>
        <p>JWT + безопасная авторизация</p>
      </div>
    </section>

  </div>
</template>
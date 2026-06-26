<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\LandingView.vue -->
<template>
  <div class="min-h-screen flex flex-col bg-slate-50">

    <!-- NAVBAR -->
    <header
      class="flex justify-between items-center px-4 sm:px-6 lg:px-10 py-4 lg:py-6 border-b bg-white"
    >

      <div class="text-2xl font-bold text-slate-900">
        Отличник
      </div>

      <div class="space-x-4">

        <button
          @click="openLogin"
          class="text-slate-600 hover:text-black transition"
        >
          Войти
        </button>

        <button
          @click="openRegister"
          class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl transition"
        >
          Начать бесплатно
        </button>

      </div>

    </header>

    <!-- HERO -->
    <main class="flex-1 flex flex-col items-center justify-center text-center px-6">

      <h1
        class="text-3xl sm:text-4xl lg:text-5xl font-bold max-w-3xl leading-tight text-slate-900"
      >

        AI объясняет школьные темы так,
        чтобы ребёнок понял за 10 минут!

      </h1>

      <p class="mt-6 text-slate-600 text-lg max-w-2xl leading-relaxed">

        Создавайте персональные задания,
        отслеживайте прогресс
        и помогайте детям учиться быстрее.

      </p>

      <div class="mt-10 flex flex-col sm:flex-row gap-4 w-full sm:w-auto">

        <button
          @click="openRegister"
          class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-2xl text-lg transition shadow-lg"
        >
          Попробовать бесплатно
        </button>

        <button
          @click="openLogin"
          class="w-full sm:w-auto bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-2xl text-lg transition shadow-lg""
        >
          Войти
        </button>

      </div>

    </main>

    <!-- LOGIN MODAL -->
    <AuthModal
      :isOpen="loginOpen"
      @close="loginOpen = false"
    >

      <LoginModal
        @close="loginOpen = false"
        @switch="
          loginOpen = false;
          registerOpen = true;
        "
      />

    </AuthModal>

    <!-- REGISTER MODAL -->
    <AuthModal
      :isOpen="registerOpen"
      @close="registerOpen = false"
    >

      <RegisterModal
        @close="registerOpen = false"
        @switch="
          registerOpen = false;
          loginOpen = true;
        "
      />

    </AuthModal>

  </div>
</template>

<script setup>
import { ref } from "vue"

import AuthModal from "@/components/modals/AuthModal.vue"
import LoginModal from "@/components/modals/LoginModal.vue"
import RegisterModal from "@/components/modals/RegisterModal.vue"

const loginOpen = ref(false)
const registerOpen = ref(false)

const openLogin = () => {
  loginOpen.value = true
}

const openRegister = () => {
  registerOpen.value = true
}
</script>
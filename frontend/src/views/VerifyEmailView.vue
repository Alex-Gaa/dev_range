<template>
  <div class="min-h-screen flex items-center justify-center bg-slate-50 px-6">
    <div class="w-full max-w-md bg-white p-8 rounded-2xl shadow">
      <h1 class="text-2xl font-bold mb-2">Verify Email</h1>
      <p class="text-slate-500 mb-6">Enter the code sent to your email</p>

      <form @submit.prevent="submit" class="space-y-4">
        <input
          v-model="email"
          type="email"
          placeholder="Email"
          class="w-full border p-3 rounded-xl"
          :disabled="loading"
        />

        <input
          v-model="code"
          type="text"
          placeholder="Verification code"
          class="w-full border p-3 rounded-xl"
          :disabled="loading"
        />

        <div v-if="error" class="text-red-600 text-sm">{{ error }}</div>
        <div v-if="success" class="text-green-600 text-sm">{{ success }}</div>

        <button
          class="w-full bg-blue-600 text-white p-3 rounded-xl disabled:opacity-50"
          :disabled="loading || !email || !code"
        >
          {{ loading ? "Verifying..." : "Verify" }}
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()
const authStore = useAuthStore()

const email = ref("")
const code = ref("")
const error = ref("")

const submit = async () => {
  error.value = ""

  try {
    await authStore.verifyEmail(email.value, code.value)
    router.push("/dashboard")
  } catch (e) {
    error.value = e.response?.data?.detail || "Verification failed"
  }
}
</script>
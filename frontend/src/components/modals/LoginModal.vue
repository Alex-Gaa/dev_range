<script setup>
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAuthStore } from "@/stores/auth"

const authStore = useAuthStore()
const router = useRouter()

const email = ref("")
const password = ref("")
const showPassword = ref(false)

const emit = defineEmits(["close", "switch"])

const handleLogin = async () => {
  try {
    await authStore.login({
      username: email.value,
      password: password.value,
    })

    emit("close")
    router.push("/dashboard")

  } catch (e) {
    alert("Login failed")
  }
}
</script>

<template>

  <div>

    <h2 class="text-3xl font-bold mb-6">
      Login
    </h2>

    <div class="space-y-4">

      <input
        v-model="email"
        type="email"
        placeholder="Email"
        class="w-full border p-3 rounded-xl"
      />

      <!-- PASSWORD -->
      <div class="relative">

        <input
          v-model="password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Password"
          class="w-full border p-3 rounded-xl pr-12"
        />

        <button
          type="button"
          @click="showPassword = !showPassword"
          class="absolute right-4 top-3 text-slate-500"
        >
          {{ showPassword ? "🙈" : "👁️" }}
        </button>

      </div>

      <!-- FORGOT PASSWORD -->

      <div class="text-right">

        <button
          type="button"
          @click="router.push('/forgot-password')"
          class="text-sm text-blue-600 hover:underline"
        >
          Forgot password?
        </button>

      </div>

      <button
        @click="handleLogin"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl"
      >
        Login
      </button>

      <p class="text-center text-slate-500">

        No account?

        <button
          @click="emit('switch')"
          class="text-blue-600"
        >
          Register
        </button>

      </p>

    </div>

  </div>

</template>

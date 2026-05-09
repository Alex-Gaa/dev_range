<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";

const authStore = useAuthStore()

const emit = defineEmits(["close", "switch"])

const showPassword = ref(false)

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password2: "",
  role: "developer",
})

const handleRegister = async () => {
  try {
    await authStore.register(form.value)

    alert("Registration successful")

    emit("switch")

  } catch (e) {
    alert("Registration failed")
  }
}
</script>

<template>

  <div>

    <h2 class="text-3xl font-bold mb-6">
      Register
    </h2>

    <div class="space-y-4">

      <input
        v-model="form.first_name"
        type="text"
        placeholder="First name"
        class="w-full border p-3 rounded-xl"
      />

      <input
        v-model="form.last_name"
        type="text"
        placeholder="Last name"
        class="w-full border p-3 rounded-xl"
      />

      <input
        v-model="form.email"
        type="email"
        placeholder="Email"
        class="w-full border p-3 rounded-xl"
      />

      <div class="relative">

        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Password"
          class="w-full border p-3 rounded-xl pr-12"
        />

        <button
          @click="showPassword = !showPassword"
          class="absolute right-4 top-3 text-slate-500"
        >
          {{ showPassword ? '🙈' : '👁️' }}
        </button>

      </div>

      <input
        v-model="form.password2"
        :type="showPassword ? 'text' : 'password'"
        placeholder="Confirm password"
        class="w-full border p-3 rounded-xl"
      />

      <button
        @click="handleRegister"
        class="w-full bg-blue-600 hover:bg-blue-700 text-white p-3 rounded-xl"
      >
        Register
      </button>

      <p class="text-center text-slate-500">

        Already have account?

        <button
          @click="emit('switch')"
          class="text-blue-600"
        >
          Login
        </button>

      </p>

    </div>

  </div>

</template>
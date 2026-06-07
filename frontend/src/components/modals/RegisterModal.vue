<!--C:\Users\Developer\PycharmProjects\devrange\frontend\src\components\modals\RegisterModal.vue-->
<script setup>
import { ref } from "vue";
import { useAuthStore } from "@/stores/auth";
import {
  getErrorMessage,
  getFieldErrors,
  hasFieldError,
  getFieldError
} from "@/utils/errorHandler"
const authStore = useAuthStore()

const emit = defineEmits(["close", "switch"])

const showPassword = ref(false)

const fieldErrors = ref({})

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password2: "",

})
const successMessage = ref("")

const handleRegister = async () => {
  try {
    fieldErrors.value = {}
    successMessage.value = ""

    await authStore.register(form.value)

    successMessage.value =
      "Аккаунт создан. Письмо для подтверждения отправлено на почту, указанную при регистрации ."

    setTimeout(() => {
      successMessage.value = ""
      emit("switch")
    }, 2500)

  } catch (error) {
    fieldErrors.value = getFieldErrors(error)
  }
}
</script>

<template>

  <div>

    <h2 class="text-3xl font-bold mb-6">
      Register
    </h2>
    <div
      v-if="successMessage"
      class="mb-4 rounded-xl border border-green-300 bg-green-50 p-3 text-green-700"
    >
      {{ successMessage }}
    </div>


    <div class="space-y-4">

      <input
        v-model="form.first_name"
        type="text"
        placeholder="First name"
        class="w-full border p-3 rounded-xl"
      />
      <p
        v-if="hasFieldError(fieldErrors, 'first_name')"
        class="text-sm text-red-500"
      >
        {{ getFieldError(fieldErrors, 'first_name') }}
      </p>

      <input
        v-model="form.last_name"
        type="text"
        placeholder="Last name"
        class="w-full border p-3 rounded-xl"
      />
      <p
        v-if="hasFieldError(fieldErrors, 'last_name')"
        class="text-sm text-red-500"
      >
        {{ getFieldError(fieldErrors, 'last_name') }}
      </p>

      <input
        v-model="form.email"
        type="email"
        placeholder="Email"
        class="w-full border p-3 rounded-xl"
      />
      <p
        v-if="hasFieldError(fieldErrors, 'email')"
        class="text-sm text-red-500"
      >
        {{ getFieldError(fieldErrors, 'email') }}
      </p>

      <div class="relative">

        <input
          v-model="form.password"
          :type="showPassword ? 'text' : 'password'"
          placeholder="Password"
          class="w-full border p-3 rounded-xl pr-12"
        />
        <p
          v-if="hasFieldError(fieldErrors, 'password')"
          class="text-sm text-red-500"
        >
          {{ getFieldError(fieldErrors, 'password') }}
        </p>


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
      <p
        v-if="fieldErrors.non_field_errors"
        class="text-sm text-red-500"
      >
        {{ fieldErrors.non_field_errors[0] }}
      </p>

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



      <p class="text-xs text-slate-500">
        Password must contain:
      </p>

      <ul class="text-xs text-slate-500 list-disc ml-5 space-y-1">
        <li>At least 8 characters</li>
        <li>One uppercase letter (A-Z)</li>
        <li>One lowercase letter (a-z)</li>
        <li>One number (0-9)</li>
        <li>One special character (!@#$%^&*)</li>
      </ul>

    </div>

  </div>

</template>
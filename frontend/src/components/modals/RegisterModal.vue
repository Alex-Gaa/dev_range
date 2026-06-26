<!--C:\Users\Developer\PycharmProjects\devrange\frontend\src\components\modals\RegisterModal.vue-->
<script setup>
import { ref, computed } from "vue";
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
const passwordRules = computed(() => ({
  length: form.value.password.length >= 8,
  uppercase: /[A-Z]/.test(form.value.password),
  lowercase: /[a-z]/.test(form.value.password),
  number: /\d/.test(form.value.password),
  special: /[^A-Za-z0-9]/.test(form.value.password),
  match:
    form.value.password &&
    form.value.password === form.value.password2,
}))

const passwordValid = computed(() =>
  Object.values(passwordRules.value).every(Boolean)
)

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
      Регистрация
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
        placeholder="Имя"
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
        placeholder="Фамилия"
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
          placeholder="Пароль"
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
        placeholder="Повторите пароль"
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
        :disabled="!passwordValid"
        class="
          w-full
          bg-blue-600
          hover:bg-blue-700
          disabled:bg-slate-300
          disabled:cursor-not-allowed
          text-white
          p-3
          rounded-xl
        "
      >
        Регистрация
      </button>




      <p class="text-center text-slate-500">

        Уже есть аккаунт?

        <button
          @click="emit('switch')"
          class="text-blue-600"
        >
          Войти
        </button>

      </p>

      <div
        class="
          bg-slate-50
          border
          rounded-xl
          p-4
          text-sm
          text-slate-600
        "
      >
        <p class="font-semibold mb-2">
          Требования к паролю:
        </p>

        <p>
          {{ passwordRules.length ? "✅" : "❌" }}
          Минимум 8 символов
        </p>

        <p>
          {{ passwordRules.uppercase ? "✅" : "❌" }}
          Хотя бы одна заглавная буква
        </p>

        <p>
          {{ passwordRules.lowercase ? "✅" : "❌" }}
          Хотя бы одна строчная буква
        </p>

        <p>
          {{ passwordRules.number ? "✅" : "❌" }}
          Хотя бы одна цифра
        </p>

        <p>
          {{ passwordRules.special ? "✅" : "❌" }}
          Хотя бы один специальный символ
        </p>

        <p>
          {{ passwordRules.match ? "✅" : "❌" }}
          Пароли совпадают
        </p>
      </div>

    </div>

  </div>

</template>
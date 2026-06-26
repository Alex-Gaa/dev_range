<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ResetPasswordView.vue -->
<template>

  <div
    class="
      min-h-screen
      flex
      items-center
      justify-center
      bg-slate-50
      px-6
    "
  >

    <div
      class="
        w-full
        max-w-lg
        bg-white
        rounded-3xl
        shadow-xl
        p-10
      "
    >

      <h1
        class="
          text-4xl
          font-bold
          text-center
          text-slate-900
        "
      >
        Сбросить пароль
      </h1>

      <p
        class="
          mt-4
          text-center
          text-slate-500
          mb-8
        "
      >
        Введите код подтверждения из письма и придумайте новый пароль.
      </p>

      <form
        @submit.prevent="submit"
        class="space-y-5"
      >

        <div>

          <input
            v-model="email"
            type="email"
            placeholder="Введите адрес электронной почты"
            required
            class="
              w-full
              border
              p-3
              rounded-xl
            "
          />

        </div>

        <div>

          <input
            v-model="code"
            type="text"
            placeholder="Введите код подтверждения"
            required
            class="
              w-full
              border
              p-3
              rounded-xl
            "
          />

        </div>

        <div>

          <div class="relative">

            <input
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="Введите новый пароль"
              required
              class="
                w-full
                border
                p-3
                rounded-xl
                pr-12
              "
            />

            <button
              type="button"
              @click="showPassword = !showPassword"
              class="absolute right-4 top-3 text-slate-500"
            >
              {{ showPassword ? "🙈" : "👁️" }}
            </button>

          </div>

        </div>

        <div>

          <div class="relative">

            <input
              v-model="password2"
              :type="showPassword2 ? 'text' : 'password'"
              placeholder="Повторите новый пароль"
              required
              class="
                w-full
                border
                p-3
                rounded-xl
                pr-12
              "
            />

            <button
              type="button"
              @click="showPassword2 = !showPassword2"
              class="absolute right-4 top-3 text-slate-500"
            >
              {{ showPassword2 ? "🙈" : "👁️" }}
            </button>

          </div>

        </div>

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
            {{ hasMinLength ? "✅" : "❌" }}
            Минимум 8 символов
          </p>

          <p>
            {{ hasUppercase ? "✅" : "❌" }}
            Хотя бы одна заглавная буква
          </p>

          <p>
            {{ hasLowercase ? "✅" : "❌" }}
            Хотя бы одна строчная буква
          </p>

          <p>
            {{ hasNumber ? "✅" : "❌" }}
            Хотя бы одна цифра
          </p>

          <p>
            {{ hasSpecial ? "✅" : "❌" }}
            Хотя бы один специальный символ
          </p>

          <p>
            {{ passwordsMatch ? "✅" : "❌" }}
            Пароли совпадают
          </p>

        </div>

        <div
          v-if="message"
          class="
            bg-green-50
            border
            border-green-200
            text-green-700
            p-4
            rounded-xl
          "
        >
          {{ message }}
        </div>

        <div
          v-if="error"
          class="
            bg-red-50
            border
            border-red-200
            text-red-700
            p-4
            rounded-xl
          "
        >
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading || !formValid"
          class="
            w-full
            bg-green-600
            hover:bg-green-700
            disabled:bg-slate-300
            disabled:cursor-not-allowed
            text-white
            p-3
            rounded-xl
            transition
          "
        >
          {{ loading ? "Сохранение..." : "Сбросить пароль" }}
        </button>

      </form>

    </div>

  </div>

</template>

<script setup>
import {
  ref,
  computed,
  onMounted
} from "vue"

import {
  useRouter,
  useRoute
} from "vue-router"

import api from "@/api/axios"

import {
  getErrorMessage
} from "@/utils/errorHandler"

const router = useRouter()
const route = useRoute()

const email = ref("")
const code = ref("")

const password = ref("")
const password2 = ref("")

const showPassword = ref(false)
const showPassword2 = ref(false)

const loading = ref(false)

const error = ref("")
const message = ref("")

onMounted(() => {
  email.value = route.query.email || ""
  code.value = route.query.code || ""
})

const hasMinLength = computed(
  () => password.value.length >= 8
)

const hasUppercase = computed(
  () => /[A-Z]/.test(password.value)
)

const hasLowercase = computed(
  () => /[a-z]/.test(password.value)
)

const hasNumber = computed(
  () => /\d/.test(password.value)
)

const hasSpecial = computed(
  () => /[!@#$%^&*()_+=\-]/.test(password.value)
)

const passwordsMatch = computed(() => {
  if (!password2.value) return true

  return password.value === password2.value
})

const passwordValid = computed(() => {
  return (
    hasMinLength.value &&
    hasUppercase.value &&
    hasLowercase.value &&
    hasNumber.value &&
    hasSpecial.value
  )
})

const formValid = computed(() => {
  return (
    passwordValid.value &&
    passwordsMatch.value
  )
})

const submit = async () => {

  loading.value = true

  error.value = ""
  message.value = ""

  try {

    const response = await api.post(
      "/auth/password-reset/confirm/",
      {
        email: email.value,
        code: code.value,
        password: password.value,
        password2: password2.value,
      }
    )

    message.value = response.data.detail

    email.value = ""
    code.value = ""
    password.value = ""
    password2.value = ""

    setTimeout(() => {
      router.push("/")
    }, 5000)

  } catch (err) {

    error.value = getErrorMessage(err)

  } finally {

    loading.value = false
  }
}
</script>
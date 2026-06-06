<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ForgotPasswordView.vue -->
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
          text-slate-900
          text-center
        "
      >
        Forgot Password
      </h1>

      <p
        class="
          mt-4
          text-center
          text-slate-500
          mb-8
        "
      >
        Enter your email address and we'll send
        you a password reset code.
      </p>

      <form
        @submit.prevent="submit"
        class="space-y-5"
      >

        <div>

          <label
            class="
              block
              mb-2
              text-sm
              font-medium
              text-slate-700
            "
          >
            Email
          </label>

          <input
            v-model="email"
            type="email"
            required
            class="
              w-full
              border
              p-3
              rounded-xl
            "
          />

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
          :disabled="loading"
          class="
            w-full
            bg-blue-600
            hover:bg-blue-700
            text-white
            p-3
            rounded-xl
            transition
          "
        >
          {{ loading ? "Sending..." : "Send Reset Code" }}
        </button>

      </form>

    </div>

  </div>

</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const email = ref("")
const loading = ref(false)
const error = ref("")
const message = ref("")

const submit = async () => {

  loading.value = true
  error.value = ""
  message.value = ""

  try {

    const response = await axios.post(
      "http://127.0.0.1:8000/api/auth/password-reset/request/",
      {
        email: email.value
      }
    )

    message.value = response.data.detail

  } catch (err) {

    error.value =
      err.response?.data?.detail ||
      "Failed to send reset code"

  } finally {

    loading.value = false
  }
}
</script>
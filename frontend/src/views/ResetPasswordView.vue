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
        Reset Password
      </h1>

      <p
        class="
          mt-4
          text-center
          text-slate-500
          mb-8
        "
      >
        Enter the verification code from your email
        and choose a new password.
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
            Verification Code
          </label>

          <input
            v-model="code"
            type="text"
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

          <label
            class="
              block
              mb-2
              text-sm
              font-medium
              text-slate-700
            "
          >
            New Password
          </label>

          <input
            v-model="password"
            type="password"
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

          <label
            class="
              block
              mb-2
              text-sm
              font-medium
              text-slate-700
            "
          >
            Confirm Password
          </label>

          <input
            v-model="password2"
            type="password"
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
            Password requirements:
          </p>

          <p>• minimum 8 characters</p>
          <p>• one uppercase letter</p>
          <p>• one lowercase letter</p>
          <p>• one number</p>
          <p>• one special character</p>

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
            bg-green-600
            hover:bg-green-700
            text-white
            p-3
            rounded-xl
            transition
          "
        >
          {{ loading ? "Saving..." : "Reset Password" }}
        </button>

      </form>

    </div>

  </div>

</template>

<script setup>
import { ref } from "vue"
import axios from "axios"

const email = ref("")
const code = ref("")
const password = ref("")
const password2 = ref("")

const loading = ref(false)

const error = ref("")
const message = ref("")

const submit = async () => {

  loading.value = true

  error.value = ""
  message.value = ""

  try {

    const response = await axios.post(
      "http://127.0.0.1:8000/api/auth/password-reset/confirm/",
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

  } catch (err) {

    const data = err.response?.data

    if (typeof data === "object") {

      error.value = Object.values(data)
        .flat()
        .join(", ")

    } else {

      error.value = "Password reset failed"
    }

  } finally {

    loading.value = false
  }
}
</script>
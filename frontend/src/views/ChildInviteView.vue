<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildInviteView.vue -->

<template>
  <div
    class="
      min-h-screen
      bg-slate-100
      flex
      items-center
      justify-center
      p-6
    "
  >

    <div
      class="
        bg-white
        w-full
        max-w-lg
        rounded-3xl
        shadow-xl
        p-8
      "
    >

      <!-- HEADER -->
      <div class="text-center mb-8">

        <h1 class="text-3xl font-bold">
          Child Account Invitation
        </h1>

        <p class="text-slate-500 mt-3">
          Create your learning account
        </p>

      </div>

      <!-- FORM -->
      <div class="space-y-4">

        <input
          v-model="form.first_name"
          type="text"
          placeholder="First name"
          class="w-full border rounded-xl px-4 py-3"
        />

        <input
          v-model="form.last_name"
          type="text"
          placeholder="Last name"
          class="w-full border rounded-xl px-4 py-3"
        />

        <input
          v-model="form.email"
          type="email"
          placeholder="Email"
          class="w-full border rounded-xl px-4 py-3"
        />

        <!-- PASSWORD -->
        <div class="relative">

          <input
            v-model="form.password"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Password"
            class="w-full border rounded-xl px-4 py-3 pr-12"
          />

          <button
            type="button"
            @click="showPassword = !showPassword"
            class="absolute right-4 top-3 text-slate-500"
          >
            {{ showPassword ? "🙈" : "👁️" }}
          </button>

        </div>

        <!-- CONFIRM PASSWORD -->
        <div class="relative">

          <input
            v-model="form.password2"
            :type="showPassword ? 'text' : 'password'"
            placeholder="Confirm password"
            class="w-full border rounded-xl px-4 py-3 pr-12"
          />

        </div>

        <!-- ERROR -->
        <div
          v-if="error"
          class="bg-red-100 text-red-700 rounded-xl px-4 py-3 text-sm"
        >
          {{ error }}
        </div>

        <!-- SUCCESS -->
        <div
          v-if="success"
          class="bg-green-100 text-green-700 rounded-xl px-4 py-3 text-sm"
        >
          Account created successfully
        </div>

        <!-- BUTTON -->
        <button
          @click="submitInvite"
          :disabled="loading"
          class="
            w-full
            bg-blue-600
            hover:bg-blue-700
            disabled:opacity-50
            text-white
            py-3
            rounded-xl
            transition
          "
        >
          <span v-if="loading">
            Creating...
          </span>

          <span v-else>
            Create Account
          </span>
        </button>

      </div>

    </div>

  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"
import { getErrorMessage } from "@/utils/errorHandler"
import api from "@/api/axios"
import { acceptInvite } from "@/api/children"

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const error = ref("")
const success = ref(false)

/* 👁️ password toggle */
const showPassword = ref(false)

const form = ref({
  first_name: "",
  last_name: "",
  email: "",
  password: "",
  password2: "",
})

/* LOAD INVITE DATA */
onMounted(async () => {
  try {
    const res = await api.get(
      `/children/invite/${route.params.token}/`
    )

    form.value.first_name = res.data.first_name || ""
    form.value.last_name = res.data.last_name || ""
    form.value.email = res.data.email || ""

  } catch (e) {
    console.log(e)
    error.value = "Invalid or expired invite link"
  }
})

/* SUBMIT */
const submitInvite = async () => {

  error.value = ""
  loading.value = true

  try {

    await acceptInvite({
      token: route.params.token,
      ...form.value,
    })

    success.value = true

    setTimeout(() => {
      router.push("/")
    }, 1500)

  } catch (e) {

    console.error(e)

    error.value = getErrorMessage(e)

  } finally {

    loading.value = false

  }

}
</script>
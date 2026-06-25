<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\components\children\AddChildModal.vue -->

<template>
  <div class="bg-white rounded-2xl p-8 w-full max-w-lg">

    <div class="flex items-center justify-between mb-6">

      <h2 class="text-2xl font-bold">
        Добавить ребенка
      </h2>

      <button
        @click="$emit('close')"
        class="text-slate-400 hover:text-black"
      >
        ✕
      </button>

    </div>

    <form
      @submit.prevent="submit"
      class="space-y-4"
    >

      <input
        v-model="form.first_name"
        type="text"
        placeholder="Имя"
        class="w-full border rounded-xl px-4 py-3"
      />

      <input
        v-model="form.last_name"
        type="text"
        placeholder="Фамилия"
        class="w-full border p-3 rounded-xl"
      />

      <input
        v-model="form.age"
        type="number"
        placeholder="Возраст"
        class="w-full border rounded-xl px-4 py-3"
      />

      <input
        v-model="form.grade"
        type="text"
        placeholder="Класс"
        class="w-full border rounded-xl px-4 py-3"
      />

      <input
        v-model="form.email"
        type="email"
        placeholder="Email (необязательно)"
        class="w-full border p-3 rounded-xl"
      />

      <textarea
        v-model="form.interests"
        placeholder="Увлечения"
        class="w-full border rounded-xl px-4 py-3"
      />

      <label class="flex items-center gap-3">

        <input
          v-model="form.has_account"
          type="checkbox"
        />

        <span>
          Создать отдельный аккаунт для ученика
        </span>

      </label>

      <div
        v-if="error"
        class="
          bg-red-50
          border
          border-red-200
          text-red-700
          p-3
          rounded-xl
        "
      >
        {{ error }}
      </div>

      <button
        class="
          w-full
          bg-blue-600
          hover:bg-blue-700
          text-white
          py-3
          rounded-xl
        "
      >
        Создать ученика
      </button>

    </form>

  </div>
</template>

<script setup>
import { reactive } from "vue"

const emit = defineEmits([
  "submit",
  "close",
])

const { error } = defineProps({
  error: {
    type: String,
    default: "",
  },
})

const form = reactive({
  first_name: "",
  last_name: "",
  email: "",
  age: "",
  grade: "",
  interests: "",
  has_account: false,
})

const submit = () => {
  emit("submit", form)
}
</script>
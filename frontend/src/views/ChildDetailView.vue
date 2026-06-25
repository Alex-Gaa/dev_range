<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildDetailView.vue -->
<!-- ChildDetailView.vue -->
<template>
  <AppLayout>
    <div v-if="child" class="space-y-6">

      <!-- HEADER -->
      <div class="bg-white border rounded-2xl p-6">
        <h1 class="text-3xl font-bold">
          {{ child.first_name }}
        </h1>

        <p class="text-slate-500 mt-2">
          {{ formatAge(child.age) }} • {{ child.grade }} класс
        </p>
      </div>

      <!-- ACTIONS -->
      <div class="flex gap-4">

        <button
          class="border px-6 py-3 rounded-xl hover:bg-slate-50 transition"
          @click="goToProgress"
        >
          Смотреть прогресс
        </button>

        <button
          @click="showResetModal = true"
          class="
            bg-amber-600
            hover:bg-amber-700
            text-white
            px-6
            py-3
            rounded-xl
          "
        >
          Сбросить пароль ученику
        </button>

      </div>
      <div
        v-if="generatedPassword"
        class="
          bg-green-50
          border
          border-green-200
          rounded-xl
          p-4
        "
      >



        <p class="font-semibold text-green-700">
          Новый пароль ученика
        </p>

        <div class="mt-2 font-mono text-lg">
          {{ generatedPassword }}
        </div>

      </div>


      <!-- AI GENERATOR -->
      <div class="bg-white border rounded-2xl p-6">

        <div class="flex items-center justify-between mb-5">
          <h2 class="text-xl font-semibold">
            Сгенерировать задание с AI
          </h2>

          <div v-if="subscription" class="text-sm text-slate-500">
            задания с AI:
            <span class="font-semibold">{{ subscription.lessons_used }}</span>
            /
            <span class="font-semibold">{{ subscription.lessons_limit }}</span>
          </div>
        </div>

        <div class="space-y-4">

          <!-- SUBJECT -->
          <select
            v-model="aiForm.subject"
            class="w-full border rounded-xl px-4 py-3"
          >
            <option value="">Выберите предмет</option>

            <option
              v-for="subject in subjects"
              :key="subject.id"
              :value="subject.id"
            >
              {{ subject.name }}
            </option>
          </select>

          <!-- TOPIC -->
          <select
            v-model="aiForm.topic"
            class="w-full border rounded-xl px-4 py-3"
          >
            <option value="">Выберите тему</option>

            <option
              v-for="topic in topics"
              :key="topic.id"
              :value="topic.name"
            >
              {{ topic.name }}
            </option>
          </select>

          <!-- CHILD INFO -->
          <div class="bg-slate-50 border rounded-xl p-4 text-sm text-slate-600">
            <p><span class="font-semibold">Возраст:</span> {{ child.age }}</p>
            <p class="mt-1"><span class="font-semibold">Класс:</span> {{ child.grade }}</p>
            <p class="mt-1">
              <span class="font-semibold">Интересы:</span>
              {{ child.interests || "Не указано" }}
            </p>
          </div>

          <!-- ERROR -->
          <div
            v-if="aiError"
            class="bg-red-50 border border-red-200 text-red-600 rounded-xl p-4"
          >
            {{ aiError }}
          </div>

          <!-- BUTTON -->
          <button
            @click="generateLesson"
            :disabled="loadingAI"
            class="bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white px-6 py-3 rounded-xl transition"
          >
            {{ loadingAI ? "Создание задания..." : "Сгенерировать задание" }}
          </button>

        </div>
      </div>

      <!-- CREATE LESSON -->
      <div class="bg-white border rounded-2xl p-6">
        <h2 class="text-xl font-semibold mb-4">
          Создать задание самостоятельно
        </h2>

        <!-- SUBJECT -->
        <select
          v-model="newLesson.subject"
          class="w-full border rounded-xl px-4 py-3 mb-3"
        >
          <option value="">
            Select subject
          </option>

          <option
            v-for="subject in subjects"
            :key="subject.id"
            :value="subject.id"
          >
            {{ subject.name }}
          </option>
        </select>

        <!-- TOPIC -->
        <select
          v-model="newLesson.topic"
          class="w-full border rounded-xl px-4 py-3 mb-3"
        >
          <option value="">
            Select topic
          </option>

          <option
            v-for="topic in manualTopics"
            :key="topic.id"
            :value="topic.id"
          >
            {{ topic.name }}
          </option>
        </select>

        <input
          v-model="newLesson.title"
          placeholder="Название задания"
          class="w-full border rounded-xl px-4 py-3 mb-3"
        />

        <textarea
          v-model="newLesson.content"
          placeholder="Введите содержание задания..."
          class="w-full border rounded-xl px-4 py-3 mb-3"
          rows="5"
        />


        <!-- ERROR -->
        <div
          v-if="manualError"
          class="bg-red-50 border border-red-200 text-red-600 rounded-xl p-4 mb-3"
        >
          {{ manualError }}
        </div>
        <button
          @click="addLesson"
          class="bg-green-600 text-white px-6 py-3 rounded-xl hover:bg-green-700 transition"
        >
          Сохранить задание
        </button>
      </div>

      <!-- LESSONS LIST -->
      <div class="bg-white border rounded-2xl p-6">

        <div class="flex items-center justify-between mb-5">
          <h2 class="text-xl font-semibold">Задания</h2>

          <span class="text-sm text-slate-500">
            {{ lessons.length }} всего
          </span>
        </div>

        <div
          v-if="lessons.length === 0"
          class="text-slate-500 text-center py-10"
        >
          Пока нет уроков
        </div>

        <div v-else class="space-y-4">

          <div
            v-for="lesson in parsedLessons"
            :key="lesson.id"
            class="border rounded-xl p-5 hover:shadow-md cursor-pointer"
            @click="openLesson(lesson.id)"
          >
            <h3 class="font-semibold text-lg">
              {{ lesson.title }}
            </h3>

            <p class="text-slate-500 text-sm mt-2 line-clamp-3">
              {{ lesson.content.slice(0, 120) }}...
            </p>

          </div>

        </div>
      </div>

    </div>

    <!-- RESET PASSWORD MODAL -->
    <div
      v-if="showResetModal"
      class="
        fixed
        inset-0
        bg-black/40
        flex
        items-center
        justify-center
        z-50
      "
    >
      <div class="bg-white rounded-2xl p-6 w-full max-w-md">

        <h3 class="text-xl font-bold mb-3">
          Reset Password
        </h3>

        <p class="text-slate-600 mb-5">
          Сбросить пароль для
          <strong>{{ child.first_name }}</strong>?
        </p>

        <div v-if="resetError" class="bg-red-50 border border-red-200 text-red-700 p-3 rounded-xl mb-4">
          {{ resetError }}
        </div>

        <div v-if="resetSuccess" class="bg-green-50 border border-green-200 text-green-700 p-3 rounded-xl mb-4">
          {{ resetSuccess }}
        </div>

        <div class="flex justify-end gap-3">

          <button
            @click="showResetModal = false"
            class="border px-4 py-2 rounded-xl"
          >
            Отмена
          </button>

          <button
            @click="resetChildPassword"
            class="bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 rounded-xl"
          >
            Сбросить
          </button>

        </div>

      </div>
    </div>


  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted, watch } from "vue"
import { useRoute, useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"
import api from "@/api/axios"
import { getErrorMessage } from "@/utils/errorHandler"

import { useChildrenStore } from "@/stores/children"
import { useLessonsStore } from "@/stores/lessons"

const route = useRoute()
const router = useRouter()

const generatedPassword = ref("")

const showResetModal = ref(false)
const resetError = ref("")

const resetSuccess = ref("")

const childrenStore = useChildrenStore()
const lessonsStore = useLessonsStore()

const child = ref(null)

const subjects = ref([])
const topics = ref([])
const manualTopics = ref([])
const subscription = ref(null)

const loadingAI = ref(false)
const aiError = ref("")
const manualError = ref("")
const resetChildPassword = async () => {

  resetError.value = ""
  resetSuccess.value = ""

  try {

    const res = await api.post(
      `/children/${child.value.id}/reset-password/`
    )

    generatedPassword.value = res.data.new_password

    resetSuccess.value = "Пароль успешно сброшен"

    // закрываем модалку через небольшую паузу
    setTimeout(() => {
      showResetModal.value = false
    }, 800)

  } catch (e) {

    resetError.value =
      e.response?.data?.detail ||
      "Не удалось сбросить пароль"
  }
}



const newLesson = ref({
  subject: "",
  topic: "",
  title: "",
  content: ""
})

const aiForm = ref({
  subject: "",
  topic: "",
})

const lessons = computed(() => lessonsStore.lessons)

/* PARSE */
const parsedLessons = computed(() =>
  lessons.value.map(l => ({ ...l }))
)

/* LOAD TOPICS WHEN SUBJECT CHANGES */
watch(() => aiForm.value.subject, async (val) => {

  if (!val) {
    topics.value = []
    return
  }

  try {

    const res = await api.get(
      `/lessons/topics/?subject=${val}`
    )

    topics.value = res.data

  } catch (e) {

    console.error(e)
  }
})

watch(() => newLesson.value.subject, async (val) => {

  if (!val) {
    manualTopics.value = []
    return
  }

  try {

    const res = await api.get(
      `/lessons/topics/?subject=${val}`
    )

    manualTopics.value = res.data

  } catch (e) {

    console.error(e)
  }
})

onMounted(async () => {

  const id = Number(route.params.id)

  let found = childrenStore.children.find(
    c => c.id === id
  )

  if (!found) {

    const res = await api.get(
      `/children/${id}/`
    )

    found = res.data
  }

  child.value = found

  if (child.value) {

    await lessonsStore.fetchLessons(
      child.value.id
    )

    subjects.value = (
      await api.get("/lessons/subjects/")
    ).data

    subscription.value = (
      await api.get("/billing/subscription/")
    ).data
  }
})

const openLesson = (id) =>
  router.push(`/lessons/${id}`)

const goToProgress = () =>
  router.push("/progress")

const addLesson = async () => {

  manualError.value = ""

  if (!child.value) return

  if (
    !newLesson.value.subject ||
    !newLesson.value.topic ||
    !newLesson.value.title.trim()
  ) {
    manualError.value = "Заполните предмет, тему и название задания"
    return
  }

  try {

    await lessonsStore.addLesson(
      child.value.id,
      newLesson.value
    )

    newLesson.value = {
      subject: "",
      topic: "",
      title: "",
      content: ""
    }

    await lessonsStore.fetchLessons(child.value.id)

  } catch (e) {

    manualError.value = getErrorMessage(e) || "Ошибка при создании задания"
  }
}

const generateLesson = async () => {

  if (!child.value) return

  if (
    !aiForm.value.subject ||
    !aiForm.value.topic
  ) {

    aiError.value =
      "Выберете предмет и тему"

    return
  }

  loadingAI.value = true
  aiError.value = ""

  try {

    await api.post(
      "/lessons/generate/lesson/",
      {
        child_id: child.value.id,
        subject_id: aiForm.value.subject,
        topic: aiForm.value.topic,
      }
    )

    await lessonsStore.fetchLessons(
      child.value.id
    )

  } catch (e) {

    aiError.value =
      e.response?.data?.error ||
      "AI error"

  } finally {

    loadingAI.value = false
  }
}
const formatAge = (age) => {
  if (age % 100 >= 11 && age % 100 <= 14) {
    return `${age} лет`
  }

  switch (age % 10) {
    case 1:
      return `${age} год`
    case 2:
    case 3:
    case 4:
      return `${age} года`
    default:
      return `${age} лет`
  }
}
const formatStatus = s => s
const statusClass = () => ""
</script>
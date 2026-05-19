<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildDetailView.vue -->

<template>
  <AppLayout>

    <div
      v-if="child"
      class="space-y-6"
    >

      <!-- HEADER -->

      <div class="bg-white border rounded-2xl p-6">

        <h1 class="text-3xl font-bold">
          {{ child.first_name }}
        </h1>

        <p class="text-slate-500 mt-2">
          {{ child.age }} years old • Grade {{ child.grade }}
        </p>

      </div>

      <!-- ACTIONS -->

      <div class="flex gap-4">

        <button
          class="
            border
            px-6
            py-3
            rounded-xl
            hover:bg-slate-50
            transition
          "
          @click="goToProgress"
        >
          View progress
        </button>

      </div>

      <!-- AI GENERATOR -->

      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-xl font-semibold mb-5">
          Generate AI Lesson
        </h2>

        <div class="space-y-4">

          <!-- SUBJECT -->

          <select
            v-model="aiForm.subject"
            class="
              w-full
              border
              rounded-xl
              px-4
              py-3
            "
          >

            <option value="">
              Select subject
            </option>

            <option value="math">
              Mathematics
            </option>

            <option value="english">
              English
            </option>

            <option value="science">
              Science
            </option>

            <option value="history">
              History
            </option>

          </select>

          <!-- TOPIC -->

          <input
            v-model="aiForm.topic"
            placeholder="Lesson topic (example: fractions)"
            class="
              w-full
              border
              rounded-xl
              px-4
              py-3
            "
          />

          <!-- CHILD INFO -->

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

            <p>
              <span class="font-semibold">
                Age:
              </span>

              {{ child.age }}
            </p>

            <p class="mt-1">
              <span class="font-semibold">
                Grade:
              </span>

              {{ child.grade }}
            </p>

            <p class="mt-1">
              <span class="font-semibold">
                Interests:
              </span>

              {{ child.interests || "Not specified" }}
            </p>

          </div>

          <!-- ERROR -->

          <div
            v-if="aiError"
            class="
              bg-red-50
              border
              border-red-200
              text-red-600
              rounded-xl
              p-4
            "
          >
            {{ aiError }}
          </div>

          <!-- BUTTON -->

          <button
            @click="generateLesson"
            :disabled="loadingAI"
            class="
              bg-blue-600
              hover:bg-blue-700
              disabled:opacity-50
              text-white
              px-6
              py-3
              rounded-xl
              transition
            "
          >

            {{
              loadingAI
                ? "Generating..."
                : "Generate AI Lesson"
            }}

          </button>

        </div>

      </div>

      <!-- CREATE LESSON -->

      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-xl font-semibold mb-4">
          Create lesson manually
        </h2>

        <input
          v-model="newLesson.title"
          placeholder="Lesson title"
          class="
            w-full
            border
            rounded-xl
            px-4
            py-3
            mb-3
          "
        />

        <textarea
          v-model="newLesson.content"
          placeholder="Write lesson content..."
          class="
            w-full
            border
            rounded-xl
            px-4
            py-3
            mb-3
          "
          rows="5"
        />

        <button
          @click="addLesson"
          class="
            bg-green-600
            text-white
            px-6
            py-3
            rounded-xl
            hover:bg-green-700
            transition
          "
        >
          Save lesson
        </button>

      </div>

      <!-- LESSONS LIST -->

      <div class="bg-white border rounded-2xl p-6">

        <div class="flex items-center justify-between mb-5">

          <h2 class="text-xl font-semibold">
            Lessons
          </h2>

          <span class="text-sm text-slate-500">
            {{ lessons.length }} total
          </span>

        </div>

        <div
          v-if="lessons.length === 0"
          class="
            text-slate-500
            text-center
            py-10
          "
        >

          No lessons yet.
          Create or generate first lesson.

        </div>

        <div
          v-else
          class="space-y-4"
        >

          <div
            v-for="lesson in lessons"
            :key="lesson.id"
            class="
              border
              rounded-xl
              p-5
              transition-all
              hover:shadow-md
              hover:-translate-y-1
              cursor-pointer
            "
            @click="openLesson(lesson.id)"
          >

            <div class="flex items-start justify-between gap-4">

              <div class="flex-1">

                <h3 class="font-semibold text-lg">
                  {{ lesson.title }}
                </h3>

                <p class="text-slate-500 text-sm mt-2 line-clamp-3">
                  {{ lesson.content }}
                </p>

              </div>

              <!-- STATUS -->

              <div
                class="
                  px-3
                  py-1
                  rounded-full
                  text-xs
                  font-medium
                  whitespace-nowrap
                "
                :class="statusClass(lesson.status)"
              >

                {{ formatStatus(lesson.status) }}

              </div>

            </div>

            <!-- PROGRESS -->

            <div class="mt-5">

              <div class="flex justify-between text-sm mb-2">

                <span class="text-slate-500">
                  Progress
                </span>

                <span class="font-medium">
                  {{ lesson.progress }}%
                </span>

              </div>

              <div
                class="
                  w-full
                  h-2
                  bg-slate-100
                  rounded-full
                  overflow-hidden
                "
              >

                <div
                  class="
                    h-full
                    bg-blue-600
                    rounded-full
                    transition-all
                  "
                  :style="{
                    width: `${lesson.progress}%`
                  }"
                />

              </div>

            </div>

          </div>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import {
  ref,
  computed,
  onMounted,
} from "vue"

import {
  useRoute,
  useRouter,
} from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"

import api from "@/api/axios"

import { useChildrenStore } from "@/stores/children"
import { useLessonsStore } from "@/stores/lessons"

const route = useRoute()
const router = useRouter()

const childrenStore = useChildrenStore()
const lessonsStore = useLessonsStore()

const child = ref(null)

const loadingAI = ref(false)

const aiError = ref("")

/* MANUAL LESSON FORM */

const newLesson = ref({
  title: "",
  content: "",
})

/* AI FORM */

const aiForm = ref({
  subject: "",
  topic: "",
})

/* LESSONS */

const lessons = computed(() => {
  return lessonsStore.lessons
})

/* INIT */

onMounted(async () => {

  const id = Number(route.params.id)

  let found = childrenStore.children.find(
    c => c.id === id
  )

  if (!found) {

    try {

      const res = await api.get(`/children/${id}/`)

      found = res.data

    } catch (e) {

      console.error(e)
    }
  }

  child.value = found

  await lessonsStore.fetchLessons(id)
})

/* OPEN LESSON */

const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

/* GO TO PROGRESS */

const goToProgress = () => {
  router.push("/progress")
}

/* MANUAL LESSON */

const addLesson = async () => {

  if (!newLesson.value.title) return

  await lessonsStore.addLesson(
    child.value.id,
    {
      title: newLesson.value.title,
      content: newLesson.value.content,
      status: "in_progress",
      progress: 10,
    }
  )

  newLesson.value.title = ""
  newLesson.value.content = ""

  await lessonsStore.fetchLessons(
    child.value.id
  )
}

/* AI GENERATION */

const generateLesson = async () => {

  if (!child.value) return

  if (
    !aiForm.value.subject ||
    !aiForm.value.topic
  ) {

    aiError.value =
      "Please select subject and topic"

    return
  }

  loadingAI.value = true

  aiError.value = ""

  try {

    await api.post(
      "/generate/lesson/",
      {
        child_id: child.value.id,
        subject: aiForm.value.subject,
        topic: aiForm.value.topic,
      }
    )

    await lessonsStore.fetchLessons(
      child.value.id
    )

    aiForm.value.subject = ""
    aiForm.value.topic = ""

  } catch (e) {

    aiError.value =
      e.response?.data?.error ||
      "AI generation failed"

    console.error(e)

  } finally {

    loadingAI.value = false
  }
}

/* STATUS */

const formatStatus = (status) => {

  switch (status) {

    case "completed":
      return "Completed"

    case "in_progress":
      return "In Progress"

    default:
      return "Draft"
  }
}

const statusClass = (status) => {

  switch (status) {

    case "completed":
      return "bg-green-100 text-green-700"

    case "in_progress":
      return "bg-blue-100 text-blue-700"

    default:
      return "bg-slate-100 text-slate-700"
  }
}
</script>
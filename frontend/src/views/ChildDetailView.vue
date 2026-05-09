<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildDetailView.vue -->
<template>
  <AppLayout>

    <div v-if="child" class="space-y-6">

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
            bg-blue-600
            text-white
            px-6
            py-3
            rounded-xl
            hover:bg-blue-700
            transition
          "
          @click="generateLesson"
        >
          Generate AI lesson
        </button>

        <button
          class="
            border
            px-6
            py-3
            rounded-xl
            hover:bg-slate-50
            transition
          "
        >
          View progress
        </button>

      </div>

      <!-- CREATE LESSON -->
      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-xl font-semibold mb-4">
          Create lesson
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

        <h2 class="text-xl font-semibold mb-4">
          Lessons
        </h2>

        <div
          v-if="lessons.length === 0"
          class="text-slate-500"
        >
          No lessons yet. Create or generate first lesson.
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

            <div class="flex items-start justify-between">

              <div>

                <h3 class="font-semibold text-lg">
                  {{ lesson.title }}
                </h3>

                <p class="text-slate-500 text-sm mt-2 line-clamp-3">
                  {{ lesson.content }}
                </p>

              </div>

              <div
                class="
                  px-3
                  py-1
                  rounded-full
                  text-xs
                  font-medium
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
                  :style="{ width: `${lesson.progress}%` }"
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
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"

import { useChildrenStore } from "@/stores/children"
import { useLessonsStore } from "@/stores/lessons"

const route = useRoute()
const router = useRouter()

const childrenStore = useChildrenStore()
const lessonsStore = useLessonsStore()

const child = ref(null)

/* FORM */
const newLesson = ref({
  title: "",
  content: "",
})

/* LESSONS */
const lessons = computed(() => lessonsStore.lessons)

/* INIT */
onMounted(async () => {

  const id = Number(route.params.id)

  child.value = childrenStore.children.find(
    c => c.id === id
  )

  await lessonsStore.fetchLessons(id)
})

/* OPEN LESSON */
const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

/* CREATE LESSON */
const addLesson = async () => {

  if (!newLesson.value.title) return

  await lessonsStore.addLesson(child.value.id, {

    title: newLesson.value.title,

    content: newLesson.value.content,

    status: "in_progress",

    progress: 10,
  })

  newLesson.value.title = ""
  newLesson.value.content = ""
}

/* AI PLACEHOLDER */
const generateLesson = async () => {

  await lessonsStore.addLesson(child.value.id, {

    title: `AI Lesson for ${child.value.first_name}`,

    content: `
      Welcome to your AI-generated lesson.

      This is a placeholder lesson for future GPT integration.
    `,

    status: "in_progress",

    progress: 15,
  })
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
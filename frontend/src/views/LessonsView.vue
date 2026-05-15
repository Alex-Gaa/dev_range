<template>
  <AppLayout>

    <!-- HEADER -->
    <div class="mb-8">

      <h1 class="text-3xl font-bold">
        All Lessons
      </h1>

      <p class="text-slate-500 mt-2">
        Lessons from all children
      </p>

    </div>

    <!-- EMPTY -->
    <div
      v-if="!lessonsStore.lessons.length"
      class="bg-white border rounded-2xl p-10 text-center"
    >
      <h2 class="text-2xl font-semibold">
        No lessons yet
      </h2>

      <p class="text-slate-500 mt-3">
        Generate first lesson for a child
      </p>
    </div>

    <!-- LESSONS -->
    <div
      v-else
      class="grid grid-cols-1 lg:grid-cols-2 gap-6"
    >

      <div
        v-for="lesson in lessonsStore.lessons"
        :key="lesson.id"
        class="
          bg-white
          border
          rounded-2xl
          p-6
          transition-all
          hover:shadow-lg
          hover:-translate-y-1
        "
      >

        <!-- TOP -->
        <div class="flex items-start justify-between">

          <!-- LEFT -->
          <div
            class="cursor-pointer"
            @click="openLesson(lesson.id)"
          >

            <h2 class="text-xl font-semibold">
              {{ lesson.title }}
            </h2>

            <p class="text-slate-500 mt-1">
              Child:
              {{ lesson.child_name }}
            </p>

          </div>

          <!-- STATUS -->
          <div
            class="px-3 py-1 rounded-full text-sm font-medium"
            :class="statusClass(lesson.status)"
          >

            {{ formatStatus(lesson.status) }}

          </div>

        </div>

        <!-- CONTENT -->
        <div
          class="mt-5 cursor-pointer"
          @click="openLesson(lesson.id)"
        >

          <p class="text-slate-700 line-clamp-4">
            {{ lesson.content }}
          </p>

        </div>

        <!-- PROGRESS -->
        <div class="mt-6">

          <div class="flex items-center justify-between mb-2">

            <span class="text-sm text-slate-500">
              Progress
            </span>

            <span class="text-sm font-medium">
              {{ lesson.progress }}%
            </span>

          </div>

          <div
            class="
              w-full
              h-3
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

        <!-- ACTIONS -->
        <div
          v-if="!isChild"
          class="flex gap-3 mt-6"
        >

          <!-- EDIT -->
          <button
            class="
              px-4
              py-2
              rounded-xl
              bg-blue-600
              text-white
              hover:bg-blue-700
            "
            @click.stop="editLesson(lesson.id)"
          >
            Edit
          </button>

          <!-- DELETE -->
          <button
            class="
              px-4
              py-2
              rounded-xl
              bg-red-600
              text-white
              hover:bg-red-700
            "
            @click.stop="deleteLesson(lesson.id)"
          >
            Delete
          </button>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"

import { useLessonsStore } from "@/stores/lessons"
import { useAuthStore } from "@/stores/auth"

const router = useRouter()

const lessonsStore = useLessonsStore()
const authStore = useAuthStore()

/* ROLE */
const isChild = computed(() => {
  return authStore.user?.role === "child"
})

onMounted(() => {
  lessonsStore.fetchAllLessons()
})

/* OPEN */
const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

/* EDIT */
const editLesson = (id) => {
  router.push(`/lessons/${id}?edit=true`)
}

/* DELETE */
const deleteLesson = async (id) => {

  if (!confirm("Delete this lesson?")) return

  await lessonsStore.deleteLesson(id)
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